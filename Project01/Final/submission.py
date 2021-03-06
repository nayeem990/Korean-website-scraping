# importing the required modules
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time
import math
options = webdriver.ChromeOptions()
options.add_argument("headless")

pd.options.display.max_columns = 999
pd.options.display.max_rows = 999
df = pd.read_csv('New_profile_links.csv')
pl = list(df["0"])

basic_data = []
main_data = []
product_review = []
profile_all = []
#all_project = []
review_all = []
main_category = []
urls = []
project_data = []

length = len(pl)
for i in range(length):
    
    try:
        one_user = []
        print("Serial :",i)
        url = pl[i]
        print(url)

        driver = webdriver.Chrome(r'C:\Users\David\chromedriver_win32\chromedriver.exe', chrome_options=options)
        driver.get(url)
        time.sleep(5)

        ######################################### basic data section ########################################
        #basic informations
        basic = []
        source_code = driver.page_source
        soup = BeautifulSoup(source_code, 'html.parser')
    except:
        print("Error in webdriver")
        continue
    try:
        basic.append(url)

        #name
        name = soup.find_all('strong', class_ = 'userName--1ZA07')
        for n in name:
            basic.append(n.text)
            

        #category
        category = soup.find_all('strong', class_ = 'introCategory--F81Ky')
        for e in category:
            basic.append(e.text)

        #specialty   
        ba = []
        sp = soup.find_all('div', class_ = 'categoryName--1zWtA')
        for m in sp:
            ba.append(m.text)
        basic.append(ba)

        #rating
        rating = soup.find_all('div', class_ = 'itemRating--360UA itemRating--2-rFv typeLarge--1cEMN')
        for k in rating:
            km = k.text
            basic.append(km.replace("평균 평점", ""))

            #Reviews and consultations
            reviews = soup.find_all('span', class_ = 'statsNum--32OX2')
            for kk in reviews:
                basic.append(kk.text)

        #appending basic data of all user
        basic_data.append(basic)


        ######################################### main ########################################
        ### main info data for one user
        maininfo = []
        uh = ["대표자","상호명","사업자등록번호","통신판매업번호", "사업장 주소", "고객센터",'메일']

        #main section info
        nn = []
        infos = soup.find_all('ul', class_ = 'productInfoList--1-H-D')
        for f in infos:
            li = f.find_all('li')
            #each list item
            for i in range(len(li)):
                ii = li[i]
                val = uh[i]
                head = ii.find_all("span", class_ = "title--2YCH3")
                maini = ii.find_all("span", class_ = "text--1z2Eb")
                for h in head:
                    if h.text != val:
                        if [k, " "] not in nn:
                            nn.append("NA")
                    else:
                        for j in maini:
                            if j.text not in nn:
                                if j.text == None or j.text == "" or j.text == " ":
                                    nn.append("NA")
                                else:   
                                    nn.append(j.text)
        main_data.append(nn)


        ######################################### count product section ########################################
        #count product and review section
        products = []
        tt = soup.find_all('div', class_ = "list--e6w5E")
        for t in tt:  
            cc = t.find_all('a', class_='item--3Oz2i')
            for cd in cc:
                ce = cd.find_all('div', class_ = "count--2w5o6")
                for i in ce:
                    products.append(i.text)
        product_review.append(products)


        ######################################### Profile data section ########################################
        #profile informations
        profile_heading = []
        profile_text = []
        firm_name = []
        firm_text = []

        div = soup.find_all('div', class_ = 'sectionIntroduce--3_qQB')
        for heading in div: 
            indiv = heading.find_all('div', class_ = 'introduceMain--g3aND')
            for i in indiv:
                head = i.find_all('strong', class_ = 'introduceMainTitle--2MZc-')
                for h in head:
                    profile_heading.append(h.text)

                text = i.find_all('p', class_ = 'introduceText--2R5pY')
                for ii in text:
                    profile_text.append(ii.text)

        careerdiv = soup.find_all('div', class_ = ['profileCareer--3_uFh','isExpert--2GkDA'])
        for i in careerdiv:
            cd = i.find_all('div', class_ = 'profileBox--1jlog')
            for j in cd:
                cd = j.find_all('div', class_ = 'careerJob--2-hX4')
                for c in cd:
                    firm_name.append(c.text)

                cui = j.find_all('ul', class_ = 'careerList--2dpZg')
                for cc in cui:
                    firm_text.append(cc.text)

        profile_all.append([profile_heading, profile_text, firm_name, firm_text])      


        ######################################### Project data section ########################################
#          ### Project data for one user
#         projects = soup.find_all('div', class_ = 'listArea--peDdh')
#         #projects  and consultations 
#         all_project = []
#         for y in projects:
#             one = []
#             yy = y.find_all('div', class_ = 'item--1ZJSx')
#             for t in yy:
#                 project_item = []
#                 tdiv = t.find_all('div', class_ =['itemTitle--2vWBq','elip2--nFWXY'])
#                 for td in tdiv:
#                     project_title = td.text
#                     if project_title == None or project_title ="":
#                         project_item.append("")
#                     else:
#                         project_item.append(project_title)

                        
#                 ratdiv = t.find_all('div', class_ =['itemGroup--2RnIL','ItemGroup_itemGroup--1f-on'])
#                 for rd in ratdiv:
#                     ratscore = rd.find_all("div", class_ = "itemRating--360UA")
#                     for r in ratscore:
#                         b = r.text
#                         if "평균 평점" in b:
#                             b = b.replace("평균 평점", " ")
#                             if b == None or b ="":
#                                 project_item.append("")
#                             else:
#                                 project_item.append(b)
                            
                            
                            
#                     ratreview = rd.find_all("div", class_ = "itemCount--2HsJv")
#                     for rr in ratreview:
#                         c = rr.text
#                         if "후기" in c:
#                             c = c.replace("후기", " ")
#                             if c == None or c ="":
#                                 project_item.append("")
#                             else:
#                                 project_item.append(c)
                            
                            

#                 feediv = t.find_all('span', class_ =['priceInner--1HE2v'])
#                 for fd in feediv:
#                     fee = fd.find_all("span", class_=["priceNum--1rXJI","ItemPrice_priceNum--2OFHI"])
#                     for f in fee:
#                         if f.text == None or f.text ="":
#                             project_item.append("")
#                         else:
#                             project_item.append(f.text)

#                     discount = fd.find_all("em", class_="discountPercent--3n0bl")
#                     for dis in discount:
#                         if dis.text == None or dis.text ="":
#                             project_item.append("")
#                         else:
#                             project_item.append(fp.text)
                        

#                     actualPrize = fd.find_all("span", class_="beforeDiscount--W1C4G")
#                     for fp in actualPrize:
#                         if fp.text == None or fp.text ="":
#                             project_item.append("")
#                         else:
#                             project_item.append(fp.text)

#                 one.append([*project_item])   
#             all_project.append([*one])

#         proj = []
#         for i in range(len(all_project)):
#             data = all_project[i]
#             for j in range(len(data)):
#                 dj = data[j]
#                 for k in range(len(dj)):
#                     bb = dj[k]
#                     if bb == None or bb == "":
#                         proj.append(" ")
#                     else:
#                         proj.append(bb) 

#         lis = ["평균 평점","후기","판매가","원할인률","할인 전 가격", "할인률"]
#         for i in range(len(proj)):
#             for j in range(len(lis)):
#                 if lis[j] in proj[i]:
#                     proj[i] = proj[i].replace(lis[j], " ")   

#         project_data.append(proj)    


    ########################################## review section ########################################
        #review object
        review_obj = []
        reviews_user = []
        reviews_rating = []
        reviews_heading = []
        reviews_text = []

        rdiv = soup.find_all('div', class_ = "listSection--kViCl")
        for eachr in rdiv:
            ee = eachr.find_all('div', class_ = "reviewItem--1OwNO")

            for each in ee:
                name = each.find_all('span', class_ = ["item--3sQA9 ","nickname--2OOe6"])
                for nm in name:
                    if nm.text == None or nm.text == "":
                        reviews_user.append("")
                    else:
                        reviews_user.append(nm.text)

                rating = each.find_all('div', class_ = ["expertPoint--2Zrvr","expertPoint--13H3V"])
                for r in rating:
                    if r.text == None or r.text =="":
                        reviews_rating.append("")
                    else:
                        reviews_rating.append(r.text)

                head = each.find_all('div', class_ = "reviewTitle--qv3Pk")
                for r in head:
                    if r.text == None or r.text =="":
                        reviews_heading.append("")
                    else:
                        reviews_heading.append(r.text)

                commentdiv = each.find_all('p', class_ = "reviewText--28mzN")
                for ecom in commentdiv:
                    if ecom.text == None or ecom.text =="":
                        reviews_text.append("")
                    else:
                        reviews_text.append(ecom.text)

        for i in range(len(reviews_user)):
            try:
                review_obj.append(reviews_user[i])
                
                if "평점" in reviews_rating[i]:
                    rating = reviews_rating[i].replace("평점", " ")
                    review_obj.append(rating)
                else:
                    review_obj.append(reviews_rating)
                review_obj.append(reviews_heading[i])
                review_obj.append(reviews_text[i])
            except:
                continue
        
        review_all.append(review_obj)
        ######################################### driver close section ########################################

        driver.quit()
        ######################################### Final dataframe section ########################################

    except:
        continue

#try:
#Url dataframe section
# urldf = pd.DataFrame(urls)
# urldf.columns = ["Url"]

#basic dataframe section
basicdf = pd.DataFrame(basic_data)
basicdf.columns = ["Url","Name","subcategory","Specialty","Review_score","Review_count","Consultations"]

#main dataframe section
maindf = pd.DataFrame(main_data)
maindf.columns =["Representative", "Company_name", "Business_registration_number", "Mail_order_number", "Business_address", "Customer_Center",'Mail']

#product review dataframe section
prdf = pd.DataFrame(product_review)
prdf.columns =["Class_Count", "Total_User_Reviews"]

# # profile dataframe section
profiledf = pd.DataFrame(profile_all)
profiledf.columns =["Profile", "Details", "Firm", "Education/Career"]

#projects dataframe section
# projdf = pd.DataFrame(project_data)

reviewdf = pd.DataFrame(review_all)

rr = []
for i in range(math.ceil(len(reviewdf.columns)/4)):
    rr.append("Reviewer_name_"+ str(i))
    rr.append("Reviewer_rating_"+ str(i))
    rr.append("Review_heading_"+ str(i))
    rr.append("Review_text_"+ str(i)) 
    
reviewdf.columns = rr

# pp = []
# ab = math.ceil(len(projdf.columns)/6)
# for i in range(ab):
#     pp.append("Package_name_"+ str(i))
#     pp.append("Package_rating_"+ str(i))
#     pp.append("Package_taken_users_"+ str(i))
#     pp.append("Discount_price_"+ str(i)) 
#     pp.append("Off_"+ str(i))
#     pp.append("Actual_price_"+ str(i))
# projdf.columns = pp

# reviewdf.columns = rr

for i in range(len(basicdf["subcategory"])):
    if basicdf["subcategory"][i] in ['법률','노동/노무','지식재산/특허',"등기/공탁/법무",'민원/행정']:
        main_category.append(["법률", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['세금/세무','회계/감사','통관/관세','온라인 마케팅','온라인쇼핑몰','엑스퍼트 사업','경영/기술컨설팅','유통관리','가맹점창업','건축','번역/통역','날씨컨설팅','원가 분석']:
        main_category.append(["비즈니스", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['자산컨설팅','부동산 상담','손해사정','신용상담','감정평가', '경제동향/전망']:
        main_category.append(["금융/재테크", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['심리상담','영양/다이어트','MBTI ']:
        main_category.append(["건강", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['운세/사주','타로카드','작명','꿈해몽','관상','풍수']:
        main_category.append(["운세", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['펫 관리','연애','육아','명상','패션/스타일','뷰티','요리/홈쿠킹','커피/주류','인테리어','청소/세탁','교통사고 분석','자동차수리']:
        main_category.append(["생활", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['음악/악기','미술/디자인','공예/공방','무용/ 발레','방송/영화','사진','실용/방송댄스','뮤지컬/공연','낚시','원예/홈가드닝','여행','글쓰기/논술']:
        main_category.append(["취미", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['입시/진학','해외유학','대학교학습','고등학교학습','중학교학습','초등학교학습']:
        main_category.append(["교육/학습", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['영어','중국어','일본어','프랑스어', '러시아어']:
        main_category.append(["외국어학습", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['피트니스','골프','필라테스','요가','생활스포츠','자전거','수상 스포츠','동계 스포츠','유아체육']:
        main_category.append(["운동/스포츠", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['게임하우투','IT노하우','코딩','오피스문서','동영상 제작']:
        main_category.append(["IT/컨텐츠", basicdf["subcategory"][i]])

    elif basicdf["subcategory"][i] in ['라이프 코칭','취업','자기PR','공무원시험 ','자격증시험']:
        main_category.append(["자기계발", basicdf["subcategory"][i]])

    else:
        main_category.append(["네이버고객센터", basicdf["subcategory"][i]])
categorydf = pd.DataFrame(main_category)
categorydf.columns = ["Main_category", "Sub_category"]

basicdf = basicdf.drop(['subcategory'], axis = 1) 

isnewdf = pd.DataFrame([["NaN"]])
isnewdf.columns = ["New_Item"]
#merging the dataframes
frames = [isnewdf, categorydf, basicdf, maindf, prdf, profiledf, reviewdf] #projdf
df = pd.concat(frames, axis = 1)
df.to_csv("df.csv")
# except:
#     print("Error during storing data")