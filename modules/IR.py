#!/usr/bin/env python3



import json
from urllib import request
from datetime import date, timedelta


class IR:
	'''
		IR module 
	'''

	baseurl="https://api.data.gov/nasa/planetary/apod?concept_tags=True&api_key=nBU6LULSiOfryhokGBZVH6hvfu5I00WHZhtDFWLx&date={}"
	basejson='''{{"title":"{0[title]}", "explanation":"{0[explanation]}", "status":"{0[status]}""}}'''

	STARTDATE=date(2015,4,3)
	ENDDATE=date(2015,4,10)

	def __init__(self):
		self.__title=None
		self.__explanation=None
		self.__status=-1

	def getInfo(self,day):
		'''
			getInfo returns a dict contains explanation, title and status as keys, status should be 0 
			if it is a valid dict, -1 otherwise. day should be date type, call like this:
				getInfo(date(year,month,day)) where year,month and day could be just numbers.
		'''
		url=self.baseurl.format(day)
		jsontxt=None

		jdict={
			"title":self.__title,
			"explanation":self.__explanation,
			"status":self.__status,
		}
		try:
			rq=request.urlopen(url)
			jsontxt=rq.read()
		except:
			return jdict
                    
		try:	
			jsonobj=json.loads(jsontxt.decode('utf8'))
			self.__title=jsonobj['title']
			self.__explanation=jsonobj['explanation']
			self.__status=0
		except:
			return jdict

		jdict={
			"title":self.__title,
			"explanation":self.__explanation,
			"status":self.__status,
		}

		return jdict

	def getRPOD(self, startdate=None, enddate=None):
		'''
			getRPOD will be returning a tuple of dictionaries, each of which represents one RPOD date.
			pass startdate and enddate to for customized period, otherwise default value will be using.
			note that the tuple will include the data on enddate, in other words, it is a closed range.
		'''	

		startdate=startdate if startdate else self.STARTDATE
		enddate=enddate if enddate else self.ENDDATE

		lst=[]
		while startdate<=enddate:
			lst.append(self.getInfo(startdate))				
			startdate=startdate+timedelta(1)

		return tuple(lst)

def test():
	ir=IR()
	rd=ir.getInfo(date(2015,4,10))
	rpod=ir.getRPOD()
	print(rpod)
	print(rd)

if __name__ == '__main__':
	test()
