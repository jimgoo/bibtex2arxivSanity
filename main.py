import time
import argparse

import bibtexparser
import editdistance

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def save_titles(bibtex_file, username, password):

    # read bibtex file
    with open(bibtex_file) as f:
        bibtex_str = f.read()
    bib_database = bibtexparser.loads(bibtex_str)
    entries = bib_database.entries

    # connect to Arxiv Sanity
    driver = webdriver.PhantomJS()
    driver.get('http://www.arxiv-sanity.com')

    # login
    username_elem = driver.find_element_by_name("username")
    password_elem = driver.find_element_by_name("password")
    username_elem.send_keys(username)
    password_elem.send_keys(password)
    driver.find_element_by_css_selector(".btn-fancy").click()

    # search for the title of each BibTeX entry
    for e, entry in enumerate(entries):

        time.sleep(5)

        title = entry['title']

        print('-'*100)
        print('%.0f%% | BibTeX title: %s' % (100.*(e+1)/len(entries), title))

        qfield = driver.find_element_by_id('qfield')
        qfield.clear()
        qfield.send_keys(title)
        qfield.send_keys(Keys.ENTER)

        papers = driver.find_elements_by_class_name('apaper')
        imgs = driver.find_elements_by_class_name('save-icon')
        assert len(imgs) == len(papers)
        
        if len(imgs) == 0:
            print('No search results')
            continue

        site_titles = []
        for paper in papers:
            site_title = paper.find_element_by_class_name('paperdesc').find_element_by_tag_name('a').get_attribute('text')
            site_titles.append(site_title)
        distances = [editdistance.eval(title, site_title) for site_title in site_titles]

        if min(distances) > 10:
            print('No match found within threshold, closest was: %s' % site_titles[i])
            continue

        i = distances.index(min(distances))
        img = imgs[i]
        
        src = img.get_attribute('src')
        if src.endswith('saved.png'):
            print('Paper already saved')
            continue

        img.click()
        print('Saved paper with title: %s' % site_titles[i])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Save articles in a BibTex file on your Arxiv Sanity account')
    parser.add_argument('bibtex_file', type=str, help='Path to BibTex file')
    parser.add_argument('username', type=str, help='Your Arxiv Sanity username')
    parser.add_argument('password', type=str, help='Your Arxiv Sanity password')
    args = parser.parse_args()
    save_titles(args.bibtex_file, args.username, args.password)

