from bs4 import BeautifulSoup
import urllib.request
import urllib
import time
from selenium import webdriver
#for watch result
file_result=open("temp_result.txt",'w')

#this address is example of amazon site which is searching result of samsung galaxy 8  

address="https://www.amazon.com/Apple-MacBook-Display-MPXR2LL-Version/dp/B071JNRK1V/ref=sr_1_1?s=pc&ie=UTF8&qid=1502917868&sr=1-1&keywords=macbook+pro"


amazon_soup=BeautifulSoup(urllib.request.urlopen(address).read(),'html.parser')
ASIN_tag=amazon_soup.find(id="ASIN")
ASIN_value=str(ASIN_tag['value'])

#for watch result
file_result.write("ASIN : "+ASIN_value) 
file_result.write('\n')

#variables set
dic_price={}   #    key : value = market name : price
dic_address={} #    key : value = market name : url

#ASNI
dic_address['usenjoy']="http://www.usenjoy.com/item/index.html?itmst=USAM&itmcd=???"
dic_address['buyitnow']="http://www.buyitnow.co.kr/product/amazon.com/???"
dic_address['bodazone']="http://www.bodazone.com/?doc=amazon/amazon.php&ASIN=???"
dic_address['joybay']="http://www.joybay.co.kr/amazon.item/???/"
dic_address['amazon365']="http://www.amazon365.com/?doc=amazon/amazon.php&ASIN=???"
dic_address['mallbuy']="http://mallbuy.co.kr/deal/detail?url=???&shop_id=amazon&lo=#null"

#URL
buyb_address="http://www.buyb.co.kr/bb/bbGoodsDetail.php?ut_sch=???"


####ASNI or url will be put to address
file_result.write("------url-------\n")

for key in dic_address.keys() :
	 #watching result
	temp_key=key
	temp_key=str(temp_key)
	temp_value=dic_address[key]
	temp_value=str(temp_value)
	temp_value=temp_value.replace("???",ASIN_value)
	dic_address[key]=temp_value
	file_result.write(temp_key+" : "+dic_address[key])
	file_result.write('\n')

buyb_address=buyb_address.replace("???",address)
file_result.write("buyb : "+buyb_address+"\n")
dic_address['buyb']=buyb_address


#parsing start//// each market has diffrent html code thefore I differ parsing code
file_result.write("-------price------\n")
#driver set
driver =webdriver.Chrome('\\Users\\nwkim\Downloads\chromedriver_win32\chromedriver')

for key_temp in dic_address.keys():
	
	key=str(key_temp)
	won="원"
	comma=","
	file_result.write("\n")

	if(key=="usenjoy"):
		soup=BeautifulSoup(urllib.request.urlopen(dic_address[key]).read())
		soup=BeautifulSoup(urllib.request.urlopen(dic_address[key]).read())
		time.sleep(7)
		price_tag=soup.find(id="rss_estimate_info")
		if price_tag is None:
			soup=BeautifulSoup(urllib.request.urlopen(dic_address[key]).read())
			price_tag=soup.find(id="rss_estimate_info")
		price_list=price_tag.findAll('b')
		price=0

		for k in price_list:
			temp_str=k.string
			temp_str=str(temp_str)
			temp_str=temp_str.replace(won,"")
			temp_str=temp_str.replace(comma,"")
			temp_int=int(temp_str)
			price+=temp_int

		dic_price[key]=price
		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))


	if(key=="buyitnow"):
		driver.get(dic_address[key])
		time.sleep(4)
		html=driver.page_source
		soup=BeautifulSoup(html,'html.parser')
		price_tag=soup.find("span",{"class","txt-price"})
		price_str=str(price_tag)
		price_sub=price_str[price_str.find("i>")+2:price_str.find("</s")]
		price_sub=price_sub.replace(comma,"")
		price_int=int(price_sub)
		dic_price[key]=price_int

		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))

	if(key=="bodazone"):
		
		driver.get(dic_address[key])
		time.sleep(4)
		html=driver.page_source
		soup=BeautifulSoup(html,'html.parser')
		
		price=0
		price_list=[]

		price_temp=soup.find(id="Vtotal_price")
		price_str=price_temp.string
		price_list.append(price_str)
		
		price_temp=soup.find(id="Vcustoms")
		price_str=price_temp.string
		price_list.append(price_str)
		
		price_temp=soup.find(id="KVaircost")
		price_str=price_temp.string
		price_list.append(price_str)
		
		for k in price_list:
			k=k.replace(comma,"")
			k=k.replace(won,"")
			k_int=int(k)
			price+=k_int

		dic_price[key]=price
		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))	


	if(key=="joybay"):
		driver.get(dic_address[key])
		html=driver.page_source
		price=0
		soup=BeautifulSoup(html,'html.parser')
		price_tag=soup.find(id="id_item_amount")

		if price_tag is None :
			price=0
		else :
			price_real=price_tag.find("strong")
			price_str=price_real.string
			price_str=price_str.replace(comma,"")
			price=int(price_str)

		dic_price[key]=price
		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))	
	
	if(key=="amazon365"):
		driver.get(dic_address[key])
		time.sleep(4)
		html=driver.page_source
		soup=BeautifulSoup(html,'html.parser')
		
		price_list=[]
		price=0

		price_tag=soup.find(id="Vtotal_price")
		price_str=price_tag.string
		price_list.append(price_str)

		price_tag=soup.find(id="KVservicecharge")
		price_str=price_tag.string
		price_list.append(price_str)

		price_tag=soup.find(id="KVaircost")
		price_str=price_tag.string
		price_list.append(price_str)
		
		for k in price_list:
			temp_str=k.replace(comma,"")
			temp_Str=temp_str.replace(won,"")
			temp=int(temp_Str)
			price+=temp

		
		
		

		dic_price[key]=price
		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))	
			
	if(key=="mallbuy"):
		driver.get(dic_address[key])
		driver.find_element_by_xpath('//*[@id="dv"]/ul/li/table/tbody/tr/td/span/table/tbody/tr/td/span/a/img').click()
		time.sleep(4)
		html=driver.page_source
		soup=BeautifulSoup(html,'html.parser')
		price_tag=soup.find("td",{"class":"pinkbgName myTxt_darkred"})
		price_str=price_tag.string
		price_str=price_str.replace(comma,"")
		price=int(price_str)
		


		dic_price[key]=price
		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))	

	if(key=="buyb"):
		driver.get(dic_address[key])
		time.sleep(4)
		html=driver.page_source
		soup=BeautifulSoup(html,'html.parser')
		price_tag=soup.find(id="span_price")
		price_str=price_tag.string
		price_str=price_str.replace(comma,"")
		price_str=price_str.replace(won,"")
		price=int(price_str)	
		

		dic_price[key]=price
		#watching result
		file_result.write(key+"  price : "+str(dic_price[key]))	
				



file_result.write("\n end of the code\n")
file_result.close()
driver.quit()



 
