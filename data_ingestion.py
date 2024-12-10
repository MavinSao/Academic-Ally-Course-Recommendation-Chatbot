import pandas as pd
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

def create_combined_info(row):
    """
    Creates a combined text representation of course information from a DataFrame row.
    Handles missing values by replacing them with 'no data'.
    """
    fields = {
        'Title': 'title',
        'Subject': 'subject',
        'Description': 'sub_info',
        'Level': 'level',
        'Institution': 'institution',
        'About': 'about',
        'What You Will Learn': 'what_you_will_learn',
        'Syllabus': 'syllabus',
        'Skills You Will Gain': 'skills_you_will_gain',
        'Rating': 'rating',
        'Course URL': 'course_url'
    }
    
    combined_info = []
    for label, field in fields.items():
        value = row[field] if pd.notna(row.get(field, pd.NA)) else 'no data'
        combined_info.append(f"{label}: {value}")
    
    return '\n'.join(combined_info)

def create_vector_store(df, embeddings_model):
    """
    Creates a FAISS vector store from the DataFrame using the specified embeddings model.
    """
    texts = df['combined_info'].tolist()
    metadata_fields = ['title', 'sub_info', 'rating', 'subject', 'level', 'institution', 'course_url']
    metadatas = df[metadata_fields].to_dict('records')
    
    return FAISS.from_texts(texts, embeddings_model, metadatas=metadatas)

def data_ingestion(csv_path="courses_csv/combined_dataset.csv", index_path="./faiss_index"):
    """
    Main function to process course data and create a searchable vector store.
    
    Args:
        csv_path: Path to the CSV file containing course data
        index_path: Path where the FAISS index will be saved
    """
    try:
        # Initialize embeddings model
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # Load CSV data directly with pandas
        df = pd.read_csv(csv_path)
        print(f"Initially loaded {len(df)} courses from CSV")
        
        # Create combined info field
        df['combined_info'] = df.apply(create_combined_info, axis=1)
        
        print(f"before removing duplicates: {len(df)} unique courses")
        # Remove duplicates based on combined info
        df = df.drop_duplicates(subset=['combined_info'])
        print(f"After removing duplicates: {len(df)} unique courses remaining")
        
        # Create and save vector store
        vectorstore = create_vector_store(df, embeddings)
        vectorstore.save_local(index_path)
        
        print(f"Successfully saved FAISS index to {index_path}")
        
    except Exception as e:
        print(f"Error during data ingestion: {str(e)}")
        raise

if __name__ == "__main__":
    data_ingestion()