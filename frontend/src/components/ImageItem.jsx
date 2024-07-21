import { BiDislike, BiLike, BiSolidDislike, BiSolidLike } from "react-icons/bi";
import { useState, useEffect } from "react";
import ImageShow from "./ImageShow";
import axios from 'axios';

const ImageItem = ({ idImg, idx, isSelect, idxSelect, isLiked, onCheckBox, onLike, onClickImg }) => {
  const [isLike, setIsLike] = useState(isLiked);
  const [isChecked, setIsChecked] = useState(isSelect);
  const [showImageShow, setShowImageShow] = useState(false);
  const [urlImg, setUrlImg] = useState("")

  useEffect(() => {
    const fetchImageUrl = async () => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get_image_url/${idImg}`);
        setUrlImg("http://127.0.0.1:8000" + response.data.url);
      } catch (error) {
        console.error("Error fetching the image URL:", error);
      }
    };
    fetchImageUrl();
  }, [idImg]);
  
  const handleImageClick = () => {
    setShowImageShow(!showImageShow);
  };

  const handleLike = (value) => {
    if (value === isLike) {
      setIsLike(0);
      onLike(0, idx);
    } else {
      setIsLike(value);
      onLike(value, idx);
    }
  };

  const handleCheckBox = (idx) => {
    onCheckBox(idx);
    setIsChecked(!isChecked);
  };

  return (
    <div className="relative">
      <input
        type="checkbox"
        className="absolute top-0 left-0 mt-2 ml-2 cursor-pointer h-4 w-4 rounded-md"
        checked={isChecked}
        onChange={() => handleCheckBox(idx)}
      />
      <div className="absolute top-0 right-0 mt-2 mr-2 gap-2 flex">   
        <button className="text-rose-500" onClick={() => handleLike(1)}>
          {isLike === 1 ? <BiSolidLike /> : <BiLike />}
        </button>
        <button className="text-rose-500" onClick={() => handleLike(-1)}>
          {isLike === -1 ? <BiSolidDislike /> : <BiDislike />}
        </button>
      </div>
      <img
        src={urlImg}
        alt={idImg}
        className={idx === idxSelect ? " rounded-lg border-4 border-teal-500" : "border-4 hover:border-teal-500"}
        onDoubleClick ={handleImageClick}
        onClick={onClickImg}
      />
      {showImageShow && <ImageShow onClose={handleImageClick} idImg={idImg} url={urlImg} />}
    </div>
  );
};

export default ImageItem;
