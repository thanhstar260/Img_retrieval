import React, { useEffect, useState } from "react";
import ImageItem from "./ImageItem";
import imageUrls from "../../src/links/image_path.json";

const ListImageResult = ({ ImageIdArr, dis, onChangeDataRerank, K }) => {
  const [stage, setStage] = useState(0);
  const [NewImageArr, setNewImageArr] = useState([[]]);
  const [idxSelect, setIdxSelect] = useState(-1);
  const [urlList, setUrlList] = useState([]);
  const [dataReRank, setDataReRank] = useState({ stages: [] });
  const [distance, setDistance] = useState([[]]);
  const [K1, setK] = useState(K);

  useEffect(() => {
    setDistance(dis);
  }, [dis]);

  useEffect(() => {
    setK(K);
  }, [K]);

  useEffect(() => {
    const tempArr = JSON.parse(JSON.stringify(ImageIdArr));
    for (let i = 0; i < tempArr.length; i++) {
      for (let j = 0; j < tempArr[i].length; j++) {
        tempArr[i][j] = { idImg: ImageIdArr[i][j], isLike: 0, isSelect: false };
      }
    }
    setNewImageArr(tempArr);
  }, [ImageIdArr]);
  
  useEffect(() => {
    const newStages = [];
    for (let i = 0; i < ImageIdArr.length; i++) {
      newStages.push({
        ids: ImageIdArr[i],
        dis: distance[i],
        positive_list: [],
        negative_list: [],
      });
    }

    setDataReRank((prevDataReRank) => ({
      ...prevDataReRank,
      stages: newStages,
    }));
  }, [ImageIdArr, distance]);
  useEffect(() => {
    onChangeDataRerank(dataReRank);
  }, [dataReRank, onChangeDataRerank]);

  const handleStageClick = (idx) => {
    setStage(idx);
  };

  const handleLike = (value, idx) => {
    const updatedNewImageArr = [...NewImageArr];
    updatedNewImageArr[stage][idx].isLike = value;
    setNewImageArr(updatedNewImageArr);

    const clonedDataReRank = { ...dataReRank };
    var tempLike = [];
    var tempDislike = [];
    for (let i = 0; i < updatedNewImageArr.length; i++) {
      tempLike = [];
      tempDislike = [];
      for (let j = 0; j < updatedNewImageArr[i].length; j++) {
        if (updatedNewImageArr[i][j].isLike === 1)
          tempLike.push(updatedNewImageArr[i][j].idImg);
        else if (updatedNewImageArr[i][j].isLike === -1)
          tempDislike.push(updatedNewImageArr[i][j].idImg);
      }
      clonedDataReRank.stages[i].positive_list = tempLike;
      clonedDataReRank.stages[i].negative_list = tempDislike;
    }
    setDataReRank(clonedDataReRank);
  };

  const handleCheckBox = (idx) => {
    const updatedNewImageArr = [...NewImageArr];
    updatedNewImageArr[stage][idx].isSelect =
      !updatedNewImageArr[stage][idx].isSelect;
    setNewImageArr(updatedNewImageArr);
  };

  const handleSetIdxSelect = (idx) => {
    setIdxSelect(idx);
    const newUrls = NewImageArr.map((item, id) => "http://127.0.0.1:8000" + imageUrls[item[idx].idImg].slice(1));
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
        {NewImageArr[stage].slice(0, K1).map((item, idx) => (
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
        {idxSelect >= 0
          ? NewImageArr.map((stageArr, stageIdx) =>
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
            )
          : null}
      </div>
    </div>
  );
};

export default ListImageResult;
