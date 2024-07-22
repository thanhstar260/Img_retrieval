import React, { useEffect, useState } from "react";
import ImageItem from "./ImageItem";
import axios from 'axios';

const ListImageResult = ({ ImageIdArr }) => {
  const [stage, setStage] = useState(0);
  const [NewImageArr, setNewImageArr] = useState([[]]);
  const [idxSelect, setIdxSelect] = useState(-1);
  const [urlList, setUrlList] = useState([])
  
  useEffect(() => {
    const tempArr = JSON.parse(JSON.stringify(ImageIdArr));
    for (let i = 0; i < tempArr.length; i++) {
      for (let j = 0; j < tempArr[i].length; j++) {
        tempArr[i][j] = { idImg: ImageIdArr[i][j], isLike: 0, isSelect: false };
      }
    }
    setNewImageArr(tempArr);
  }, [ImageIdArr]);

  const fetchImageUrl = async (id) => {
    try {
      const response = await axios.get(`http://127.0.0.1:8000/get_image_url/${id}`);
      return ("http://127.0.0.1:8000" + response.data.url);
    } catch (error) {
      console.error("Error fetching the image URL:", error);
      return "";
    }
  };

  const handleStageClick = (idx) => {
    setStage(idx);
  };

  const handleLike = (value, idx) => {
    const updatedNewImageArr = [...NewImageArr];
    updatedNewImageArr[stage][idx].isLike = value;
    setNewImageArr(updatedNewImageArr);
  };

  const handleCheckBox = (idx) => {
    const updatedNewImageArr = [...NewImageArr];
    updatedNewImageArr[stage][idx].isSelect =
      !updatedNewImageArr[stage][idx].isSelect;
    setNewImageArr(updatedNewImageArr);
  };

  const handleSetIdxSelect = async (idx) => {
    setIdxSelect(idx);
    console.log(NewImageArr);

    const newUrls = await Promise.all(NewImageArr.map((item,id) => fetchImageUrl(NewImageArr[id][idx].idImg)));
    setUrlList(newUrls);
  };
  return (
    <div className="h-screen ">
      <div className="flex flex-row gap-4 mb-2">
        {ImageIdArr.map((item, idx) => (
          <button
            key={`stage${idx}`}
            className={`hover:text-teal-500 ${
              stage === idx ? "text-teal-500" : "text-black"
            }`}
            onClick={() => handleStageClick(idx)}
          >
            Stage {idx + 1}
          </button>
        ))}
      </div>
      <div className="w-full grid grid-cols-6 overflow-y-scroll h-3/5 mb-2">
        {NewImageArr[stage].map((item, idx) => (
          <ImageItem
            key={`${stage}-${idx}`}
            idImg={item.idImg}
            idx={idx}
            isSelect={item.isSelect}
            isLiked={item.isLike}
            idxSelect={idxSelect}
            onCheckBox={(value) => handleCheckBox(idx)}
            onLike={(value) => handleLike(value, idx)}
            onClickImg={(value) => handleSetIdxSelect(idx)}
          />
        ))}
      </div>
      <div className="border border-teal-500 p-1 h-40 flex gap-2 overflow-x-scroll">
        {idxSelect>=0? NewImageArr.map((stageArr, stageIdx) =>
          stageArr.map((item, idx) =>
            idx === idxSelect ? (
              <img
                key={`bottom-${stage}-${idx}`}
                src={urlList[stageIdx]}
                alt={item.idImg}
                className="max-h-full max-w-full h-auto border-4 hover:border-teal-500"
              />
            ) : null
          )
        ): null}
      </div>
    </div>
  );
};

export default ListImageResult;
