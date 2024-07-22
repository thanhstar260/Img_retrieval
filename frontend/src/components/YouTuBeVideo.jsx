import { useEffect, useState } from "react";
import React from "react";
import axios from "axios";

const YouTubeVideo = ({ idImg }) => {
  const [urlVideo, setUrlVideo] = useState("");

  useEffect(() => {
    const fetchVideoUrl = async () => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/get_video_url/${idImg}`
        );
        setUrlVideo(response.data.url);
      } catch (error) {
        console.error("Error fetching the image URL:", error);
      }
    };
    fetchVideoUrl();
  }, [idImg]);
  return (
    <div>
      <iframe
        width="650"
        height="400"
        src={urlVideo}
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin"
        allowfullscreen
      ></iframe>
    </div>
  );
};

export default YouTubeVideo;
