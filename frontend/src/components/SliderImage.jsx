import Slider from "react-slick";
import React, { useState, useEffect } from "react";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import axios from "axios";

function SampleNextArrow(props) {
  const { className, style, onClick, updateImgIdArr } = props;
  return (
    <div
      className={className}
      style={{
        ...style,
        display: "flex",
        background: "green",
        borderRadius: "50%",
        width: "30px",
        height: "30px",
        justifyContent: "center",
        alignItems: "center",
      }}
      onClick={() => {
        updateImgIdArr(1);
        onClick();
      }}
    />
  );
}

function SamplePrevArrow(props) {
  const { className, style, onClick, updateImgIdArr } = props;
  return (
    <div
      className={className}
      style={{
        ...style,
        display: "flex",
        background: "green",
        borderRadius: "50%",
        width: "30px",
        height: "30px",
        justifyContent: "center",
        alignItems: "center",
      }}
      onClick={() => {
        updateImgIdArr(-1);
        onClick();
      }}
    />
  );
}
const SliderImage = ({ idImg, onArrow }) => {
  const [ImgIdArr, setImgIdArr] = useState([
    idImg - 2,
    idImg - 1,
    idImg,
    idImg + 1,
    idImg + 2,
  ]);
  const [urlImgArr, setUrlImgArr] = useState(["", "", "", "", ""]);
  
  useEffect(() => {
    const fetchImageUrl = async (id) => {
      try {
        const response = await axios.get(`http://127.0.0.1:8000/get_image_url/${id}`);
        return ("http://127.0.0.1:8000" + response.data.url);
      } catch (error) {
        console.error("Error fetching the image URL:", error);
        return "";
      }
    };
    const fetchAllImages = async () => {
      const newUrls = await Promise.all(ImgIdArr.map(id => fetchImageUrl(id)));
      setUrlImgArr(newUrls);
    };

    fetchAllImages();
  }, [ImgIdArr]);
  

  const [index, setIndex] = useState(2);
  const updateImgIdArr = (increment) => {
    const newImgIdArr = ImgIdArr.map((item) => item + increment);
    var newIndex = index;
    if (increment === 1) {
      const lastElement = newImgIdArr.pop();
      newImgIdArr.unshift(lastElement);
      if (index + 1 === 5) {
        newIndex = 0;
        setIndex(0);
      } else {
        newIndex = newIndex + 1;
        setIndex(newIndex);
      }
    } else {
      const firstElement = newImgIdArr.shift();
      newImgIdArr.push(firstElement);
      if (index - 1 === -1) {
        newIndex = 4;
        setIndex(4);
      } else {
        newIndex = newIndex - 1;
        setIndex(newIndex);
      }
    }
    setImgIdArr(newImgIdArr);
    onArrow(newImgIdArr[newIndex]);
  };

  const settings = {
    draggable: false,
    dots: false,
    infinite: true,
    speed: 100,
    slidesToShow: 5,
    slidesToScroll: 1,
    nextArrow: <SampleNextArrow updateImgIdArr={updateImgIdArr} />,
    prevArrow: <SamplePrevArrow updateImgIdArr={updateImgIdArr} />,
  };
  return (
    <div className="w-2/3">
      <Slider {...settings}>
        {ImgIdArr.map((item, idx) => (
          <div key={`slider${idx}`} className="px-2 py-1">
            <img
              src={urlImgArr[idx]}
              className={
                idx === index ? " rounded-lg border-4 border-teal-500" : ""
              }
              alt={ImgIdArr[idx]}
            />
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default SliderImage;
