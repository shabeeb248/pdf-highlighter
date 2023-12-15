

import streamlit as st
import requests
import json
import fitz 
import os

isExist = os.path.exists("Input folder")
if not isExist:
    os.makedirs("Input folder", exist_ok=True)

isExist = os.path.exists("Working folder")
if not isExist:
    os.makedirs("Working folder", exist_ok=True) 

isExist = os.path.exists("Output folder")
if not isExist:
    os.makedirs("Output folder", exist_ok=True)  


list_1 = [' freeze ', ' froze ', ' frozen ', ' freezing ', ' cease ', ' ceasement ', ' cessation ', ' ceasing ', 
          ' ceased ', ' ceases ', ' halt ', ' halted ', ' stop ', ' stopped ', ' restructure ', ' restructuring ', 
          ' restructured ', ' conversion ', ' converted ', ' replacement ', ' replace ', ' replaced ', ' redesign ', 
          ' redesigned ', ' renegotiate ', ' renegotiated ', ' end ', ' ended ', ' terminate ', ' terminated phase out ', 
          ' phased out ', ' convert ', ' converted ', ' replace ', ' replaced ', ' revise ', ' revised change ', 
          ' changed ', ' changes ', ' stop ', ' stopped ', ' discontinue discontinued ', ' end ', ' shutdown ', 
          ' prevent ', ' prevented ', ' prevented close ', ' closed ', ' transitioned ', ' transition ', 
          ' transitioning ', ' lump sum ', ' annuity ', ' convert ', ' converted ', ' converting ', ' amend ', 
          ' amended amending ', ' amendment ', ' amendments ', ' no future ', ' lump sum ', ' eligible ', 
          ' terminated ', ' terminate no longer ', ' no future ', ' not eligible ', ' not participate ', ' covered ', ' cover ']

list_2 = [' defined ', ' defined benefit ', ' pension ', ' postretirement ', ' postemployment ', ' retirement ', 
          ' benefit ', ' benefits ', ' new ', ' defined contribution ', ' contributions ', ' future ', ' benefits ', 
          ' accruals ', ' employees ', ' employee ', ' participants ', ' plans ', ' plan ', ' 401(k) ', ' 401 ', 
          ' contributions ', ' contribution ', ' effective ', ' benefit ', ' plans ', ' Participant ', ' effective ', 
          ' participants ', ' hires ', ' entrants ', ' retirement ']



def highlight_keyword_in_pdf(file_name,keywords_1,keywords_2):
    input_pdf_path="/content/input_pdf/"+file_name
    document = fitz.open(input_pdf_path)
    print("File Name : ",file_name)
    print("\n")
    page_n_list = []
    for page_number in range(len(document)):
        insta_heiglate_1=[]
        insta_heiglate_2=[]
        page = document[page_number]
        for k in keywords_1:
          text_instances_1 = page.search_for(k)
          if text_instances_1:
            for j in keywords_2:
              text_instances_2 = page.search_for(j)
              if text_instances_2:
                  for item in text_instances_1:
                      insta_heiglate_1.append(item)
                  for item in text_instances_2:
                    insta_heiglate_2.append(item)
                    page_n_list.append(page_number)
                  print(" #Page No : ", page_number+1)  
                  print("     Keyword_1 : ",j)
                  print("     Keyword_2 : ",k)
                  print("              ")

        unique_list_1 = list(set(insta_heiglate_1))
        unique_list_2 = list(set(insta_heiglate_2))
        page_n_list_final = list(set(page_n_list))
        for inst_1 in unique_list_1:
              highlight = page.add_highlight_annot(inst_1)
              highlight.set_colors({"stroke":(1, 0.5, 0.5)})
              highlight.update()
        for inst_2 in unique_list_2:
              highlight = page.add_highlight_annot(inst_2)
              highlight.set_colors({"stroke":(1, 0.5, 0.5)})
              highlight.update()
        

        
    print("-----------------------------------------------------------------------")
    output_pdf_path="/content/output_pdf/"+file_name   
    document.save(output_pdf_path)
    document.close()
    return page_n_list,output_pdf_path



def annotate_text_on_page(input_pdf_path, output_pdf_path, page_lis):
    document = fitz.open(input_pdf_path)

    
    for page_number in page_lis:
      if page_number < 0 or page_number >= len(document):
        print(f"Page number {page_number} is out of range.")
        return
      page = document[page_number]

      text_blocks = page.get_text("blocks")

      for block in text_blocks:
          rect = fitz.Rect(block[:4])  
          page.add_highlight_annot(rect)

    document.save(output_pdf_path)


if "text" not in st.session_state:
    st.session_state.text = ""

if "loading" not in st.session_state:
    st.session_state.loading = False


st.set_page_config(page_title="pdf highlighter", page_icon=":speech_balloon:")


uploaded_files = st.sidebar.file_uploader("Upload a files to pinecone", key="file_uploader",accept_multiple_files=True, type="pdf")
if st.sidebar.button("Upload File"):
    if uploaded_files:
       if st.button('Extract Data'):
          with st.spinner('Extracting data...'):
             for file in uploaded_files:
                    final_output_pdf_path="final_output/"+file.name 
                    print(final_output_pdf_path)
                    pag_lis,out_path=highlight_keyword_in_pdf(file, list_1,list_2)
                    if(len(pag_lis)>0):
                        annotate_text_on_page(out_path,final_output_pdf_path,pag_lis)  
                        os.remove(file.name)

        #   st.write(final)



# if uploaded_files:
#     if st.button('Extract Data'):
#         with st.spinner('Extracting data...'):
#             final= get_final_data(prompt_in)
#         st.write(final)

