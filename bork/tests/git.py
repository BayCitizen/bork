from ..git_reqs import GitReq

try:
	r=GitReq(self, repo=None, dest=None, branch=None,  *args, **kwargs):)
	r.statisfy()
except, e: 
	print 'Git req test: ', args, 'args'
	print e
	print 'test failed'
    