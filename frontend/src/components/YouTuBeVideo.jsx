import { useEffect, useState } from "react";
import React from "react";
import videoUrls from "../../src/links/id2link_convert.json";

const YouTubeVideo = ({ idImg }) => {
  const [urlVideo, setUrlVideo] = useState("");

  useEffect(() => {
    const url = videoUrls[idImg];
    setUrlVideo(url);
  }, [idImg]);

  return (
    <div>
      <iframe
        width="720"
        height="405"
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
