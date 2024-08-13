import { useState, useEffect, useContext } from "react";
import { IoMdCloseCircleOutline } from "react-icons/io";
import { ImYoutube2 } from "react-icons/im";
import SliderImage from "./SliderImage";
import YouTubeVideo from "./YouTuBeVideo";
import { RxReset } from "react-icons/rx";
import { IoMdSearch } from "react-icons/io";
import imageUrls from "../../src/links/image_path.json";

import { DataContext } from './DataContext';

const ImageShow = ({ idImg, onClose, url }) => {
  const [showVideo, setShowVideo] = useState(false);
  const [NewShowIdImg, setNewShowIdImg] = useState(idImg);
  const [urlImg, setUrlImg] = useState(url)
  const [toggle, setToggle] = useState(true);

  const {ids, setIds, dis, setDis} = useContext(DataContext);


  useEffect(() => {
    const url = imageUrls[NewShowIdImg];
    setUrlImg("http://127.0.0.1:8000" + url.slice(1));
  }, [NewShowIdImg]);

  const handleShowVideo = () => {
    setShowVideo(!showVideo);
  };

  const handleNewShowIdImg = (newId) => {
    setNewShowIdImg(newId);
  };
  const handleResetId = () => {
    setNewShowIdImg(idImg);
    setToggle(!toggle);
  };

  const searchByImage= async (id)=>{
    const response =  await fetch('http://127.0.0.1:8000/searchbyimg', {
      headers: {
        'Content-type': 'application/json'
      },
      method: 'POST',
      body: JSON.stringify({message: imageUrls[id]})
    });
    const json = await response.json();
    setIds([json.ids]);
    setDis([json.dis]);
    onClose();
  }
  return (
    <div
      className="fixed flex flex-col top-0 left-0 right-0 bottom-0 pt-14 bg-black bg-opacity-75 z-50"
      onClick={onClose}
    >
      <button
        className="absolute top-5 right-5 text-white hover:text-teal-500"
        onClick={onClose}
      >
        <IoMdCloseCircleOutline size={50} />
      </button>
      <div
        className="max-w-3/4 relative flex flex-col items-center"
        onClick={onClose}
      >
        <div className="w-fit mb-12" onClick={(e) => e.stopPropagation()}>
          {!showVideo ? (
            <img
              src={urlImg}
              alt={NewShowIdImg}
              style={{width: "720px", height: "auto"}}
            />
          ) : (
            <YouTubeVideo idImg={NewShowIdImg} />
          )}
          <div className="flex justify-between mt-2">
            <button
              className="text-red-500 rounded-lg px-4 bg-white mt-2 "
              onClick={handleShowVideo}
            >
              <ImYoutube2 size={40} />
            </button>
            {!showVideo && (
              <button
                className="text-rose-500 rounded-lg px-4 bg-white mt-2 hover:text-white hover:bg-rose-500"
                onClick={()=>searchByImage(NewShowIdImg)}
              >
                <IoMdSearch size={40} />
              </button>
            )}
            {!showVideo && (
              <button
                className="text-rose-500 rounded-lg px-4 bg-white mt-2 hover:text-white hover:bg-rose-500"
                onClick={handleResetId}
              >
                <RxReset size={40} />
              </button>
            )}
          </div>
        </div>
      </div>
      <div
        onClick={(e) => e.stopPropagation()}
        className="flex flex-row justify-center"
      >
        <SliderImage
          idImg={NewShowIdImg}
          key={toggle}
          onArrow={handleNewShowIdImg}
        />
      </div>
    </div>
  );
};

export default ImageShow;
