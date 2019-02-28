
from bs4 import BeautifulSoup


def from_result_content(content):
    """ Get the couple information from a competition result page.

    Example URL: http://www.csts.cz/cs/VysledkySoutezi/Par/307
    Only the page content text should be passed to this function. Result is
    a pair, first item is the leader, second item is the follower.
    """
    bs = BeautifulSoup(content, 'lxml')
    couple_div = bs.div.findAll('div')[1]
    links = couple_div.find_all('a')
    couple_div.prettify()
    couple_div.prettify()
    leader_html, snd = couple_div.decode_contents().split('&amp;')
    follower_html, club_html = snd.split(' - ')

    def dancer_from_html(text, club):
        bs = BeautifulSoup(text, 'lxml')
        club = club.strip()
        if bs.find('a'):
            return {'id': int(bs.a['href'].split('/')[-1]), 'name': bs.a.text.strip(), 'club': club }
        else:
            return { 'name': bs.text.strip(), 'club': club }

    return dancer_from_html(leader_html, club_html), dancer_from_html(follower_html, club_html)


def hash(dancer):
    """ Return a unique identifier for a dancer that can be used to key dictionaries. """
    if 'id' in dancer.keys():
        return dancer['id']
    else:
        return dancer['name']


def test():
    content_cz = open('data/pary/000000/000001.html').read()
    content_sk = open('data/pary/000000/000307.html').read()
    leader_cz, follower_cz = from_result_content(content_cz)
    leader_sk, follower_sk = from_result_content(content_sk)
    hash(leader_cz)
    hash(leader_sk)
