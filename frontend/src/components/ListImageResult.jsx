import React, { useEffect, useState } from "react";
import ImageItem from "./ImageItem";

const ListImageResult = ({ ImageIdArr }) => {
  const [stage, setStage] = useState(0);
  const [NewImageArr, setNewImageArr] = useState([[]]);
  const [idxSelect, setIdxSelect] = useState(0);

  useEffect(() => {
    const tempArr = JSON.parse(JSON.stringify(ImageIdArr));
    for (let i = 0; i < tempArr.length; i++) {
      for (let j = 0; j < tempArr[i].length; j++) {
        tempArr[i][j] = { idImg: ImageIdArr[i][j], isLike: 0, isSelect: false };
      }
    }
    setNewImageArr(tempArr);
  }, [ImageIdArr]);

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

  const handleSetIdxSelect = (idx) => {
    setIdxSelect(idx);
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
        {NewImageArr.map((stageArr, stageIdx) =>
          stageArr.map((item, idx) =>
            idx === idxSelect ? (
              <img
                key={`bottom-${stage}-${idx}`}
                src="./id1.jpg"
                alt={item.idImg}
                className="max-h-full max-w-full h-auto border-4 hover:border-teal-500"
              />
            ) : null
          )
        )}
      </div>
    </div>
  );
};

export default ListImageResult;
