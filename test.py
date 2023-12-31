from text import load_clip_feature, load_image_path, load_model, create_faiss_index, text2img, visualize
# from image import load_clip_feature, load_image_path, load_model, create_faiss_index, img2img, visualize
import torch


# DEFINE PARAMETER

feature_folder_path = r'C:\Users\admin\Projects\AIC\DATA\clip-features-vit-b32'
image_path_dict = r"C:\Users\admin\Projects\AIC\image_path.json"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
K = 40

img_query_path = r"C:\Users\admin\Projects\AIC\DATA\Keyframes\Keyframes_L01\L01_V002\0019.jpg"
text_query = "a dolphin and a pink ball"

# LOAD CLIP_FEATURE
clip_feature = load_clip_feature(feature_folder_path)

# LOAD IMG_PATH
image_path = load_image_path(image_path_dict)

# LOAD MODEL
model,preprocess = load_model(device)

# CREATE FAISS INDEX
vector_db = create_faiss_index(clip_feature)

# TEST Query

result = text2img(model, text_query, K, device,vector_db)
# result = img2img(preprocess,model,img_query_path,K,device,vector_db)
visualize(result, K, image_path)