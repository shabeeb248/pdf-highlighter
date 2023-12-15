import streamlit as st
import fitz 
import os
import pandas as pd
import shutil
# Ensure necessary directories exist
directories = ["Input folder", "Working folder", "Output folder"]
def deleteOutput():
    folder = 'Output Folder'
    file_path='downloads.zip'
    if os.path.isfile(file_path) or os.path.islink(file_path):
        os.unlink(file_path)
    elif os.path.isdir(file_path):
        shutil.rmtree(file_path)
    if os.path.exists(folder):
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
    # st.success("Deletion ÷Completed")


for dir in directories:
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)

# Keyword lists
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


# Function to highlight keywords in PDF
# def highlight_keyword_in_pdf(file_name, keywords_1, keywords_2):
#     input_pdf_path = os.path.join("Input folder", file_name)
#     output_pdf_path = os.path.join("Output folder", file_name)
    
#     document = fitz.open(input_pdf_path)
#     page_n_list = []

#     for page_number in range(len(document)):
#         page = document[page_number]
#         for k in keywords_1:
#             text_instances_1 = page.search_for(k)
#             for j in keywords_2:
#                 text_instances_2 = page.search_for(j)
#                 if text_instances_1 and text_instances_2:
#                     page_n_list.append(page_number)
#                     highlight_instances(page, text_instances_1, (1, 0.5, 0.5)) # Highlight color can be changed
#                     highlight_instances(page, text_instances_2, (0.5, 1, 0.5)) # Different color for second set of keywords

#     document.save(output_pdf_path)
#     document.close()
#     return page_n_list, output_pdf_path

# # Helper function to highlight instances
# def highlight_instances(page, instances, color):
#     for inst in instances:
#         highlight = page.add_highlight_annot(inst)
#         highlight.set_colors({"stroke": color})
#         highlight.update()

# # Streamlit UI
# st.set_page_config(page_title="PDF Highlighter", page_icon=":speech_balloon:")

# uploaded_files = st.sidebar.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")

# if uploaded_files and st.sidebar.button("Highlight Keywords"):
#     with st.spinner('Highlighting keywords in PDF...'):
#         for uploaded_file in uploaded_files:
#             # Save the uploaded file to the input folder
#             input_file_path = os.path.join("Input folder", uploaded_file.name)
#             with open(input_file_path, "wb") as f:
#                 f.write(uploaded_file.getbuffer())
            
#             # Process the PDF file
#             page_list, output_pdf_path = highlight_keyword_in_pdf(uploaded_file.name, list_1, list_2)
#             st.success(f"Keywords highlighted in {uploaded_file.name}.")
#             st.write(f"Pages with keywords: {page_list}")
#             st.download_button(label="Download Highlighted PDF", data=open(output_pdf_path, "rb"), file_name=uploaded_file.name, mime="application/pdf")

def highlight_keyword_in_pdf(file_name, keywords_1, keywords_2):
    input_pdf_path = os.path.join("Input folder", file_name)
    output_pdf_path = os.path.join("Output folder", file_name)
    
    document = fitz.open(input_pdf_path)
    highlights_data = []

    for page_number in range(len(document)):
        page = document[page_number]
        for k in keywords_1:
            text_instances_1 = page.search_for(k)
            for j in keywords_2:
                text_instances_2 = page.search_for(j)
                if text_instances_1 and text_instances_2:
                    highlight_instances(page, text_instances_1, (1, 0.5, 0.5)) # Highlight color can be changed
                    highlight_instances(page, text_instances_2, (0.5, 1, 0.5)) # Different color for second set of keywords
                    for inst in text_instances_1 + text_instances_2:
                        highlights_data.append([file_name, page_number + 1, k.strip(), j.strip()])

    document.save(output_pdf_path)
    document.close()
    return highlights_data, output_pdf_path

# Helper function to highlight instances
def highlight_instances(page, instances, color):
    for inst in instances:
        highlight = page.add_highlight_annot(inst)
        highlight.set_colors({"stroke": color})
        highlight.update()

# Streamlit UI
st.set_page_config(page_title="PDF Highlighter", page_icon=":speech_balloon:")
deleteOutput()


uploaded_files = st.sidebar.file_uploader("Upload PDF files", accept_multiple_files=True, type="pdf")
all_highlights = []

if uploaded_files and st.sidebar.button("Highlight Keywords"):
    with st.spinner('Highlighting keywords in PDF...'):
        for uploaded_file in uploaded_files:
            # Save the uploaded file to the input folder
            input_file_path = os.path.join("Input folder", uploaded_file.name)
            with open(input_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Process the PDF file
            highlights_data, output_pdf_path = highlight_keyword_in_pdf(uploaded_file.name, list_1, list_2)
            all_highlights.extend(highlights_data)
            st.success(f"Keywords highlighted in {uploaded_file.name}.")
   
            # st.download_button(label="Download Highlighted PDF", data=open(output_pdf_path, "rb"), file_name=uploaded_file.name, mime="application/pdf")
    
if all_highlights:
    # Create a DataFrame and display it
    df = pd.DataFrame(all_highlights, columns=["File Name", "Page Number", "Keyword 1", "Keyword 2"])
    st.dataframe(df)

    # Convert DataFrame to CSV and create download link
    csv = df.to_csv(index=False).encode('utf-8')
    csv = df.to_csv("Output Folder/a.csv")
    shutil.make_archive('downloads', 'zip', "Output Folder")
    st.download_button(label=f"Download", data=open('downloads.zip', "rb"), file_name='output.zip', mime="application/zip")


    # csv.save()
    # st.download_button(label="Download Highlight Details as CSV", data=csv, file_name="highlight_details.csv", mime="text/csv")

# if os.path.exists("Output Folder"):
#         if st.button("Convert Output Folder to ZIP"):
#             shutil.make_archive('downloads', 'zip', "Output Folder")
#             st.download_button(label=f"Download ", data=open('downloads.zip', "rb"), file_name='1.zip', mime="application/zip")

        # out_files = os.listdir("Output Folder")
        # if len(out_files)>0:
        #     st.write("Output Folder has data. Delete if you want to generate new data")
        #     if(st.button("Delete Output Files")):
        #         os.rem
        # for i in out_files:
        #     output_pdf_path = os.path.join("Output folder", i)
        #     st.download_button(label=f"Download Highlighted PDF {i}", data=open(output_pdf_path, "rb"), file_name=i, mime="application/pdf")
# if st.button("Convert Output Folder to ZIP"):
#     shutil.make_archive('downloads', 'zip', "Output Folder")
#     st.download_button(label=f"Download", data=open('downloads.zip', "rb"), file_name='1.zip', mime="application/zip")
