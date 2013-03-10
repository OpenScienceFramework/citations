import pycurl

c = pycurl.Curl()
citation = 'Albertson, K., & Shore, C. (2009). Holding in mind conflicting information: Pretending, working memory, and executive control. Journal of Cognition and Development, 9, 390-410. doi: 10.1080/15248370802678240'
c.setopt(c.URL, 'http://freecite.library.brown.edu/citations/create')
c.setopt(c.POSTFIELDS, 'Accept=text/xml&citation=%s' % citation)
c.perform()

