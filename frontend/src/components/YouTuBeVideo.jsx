import React from "react";

const YouTubeVideo = (idImg) => {
  return (
    <div>
      <iframe
        width="650"
        height="400"
        src="https://www.youtube.com/embed/kouc4BoGG8c?si=MrbEeL-2_Rw9Jbn3&start=120"
        title="YouTube video player"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin"
      ></iframe>
    </div>
  );
};

export default YouTubeVideo;
