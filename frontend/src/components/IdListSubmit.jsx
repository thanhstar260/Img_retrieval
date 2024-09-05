import React, { useEffect, useState } from "react";
import { FaFileDownload } from "react-icons/fa";
import { MdDeleteOutline } from "react-icons/md";
import imageUrls from "../../src/links/image_path.json";

const IdListSubmit = ({ listId, ClearID }) => {
  const [videoName, setVideoName] = useState([]);

  useEffect(() => {
    const names = [];

    for (let i = 0; i < listId.length; i++) {
      var parts = imageUrls[listId[i]].split("/");
      names.push(parts[parts.length - 2]);
    }
    setVideoName(names);
  }, [listId]);

  const DownloadID = () => {
    let savedIds = [];
    if (localStorage.getItem("submitIds")) {
      savedIds = JSON.parse(localStorage.getItem("submitIds"));
      if (savedIds.length === 0) return;
    } else {
      return;
    }
    const element = document.createElement("a");
    const combinedArray = savedIds.map((id, index) => `${id}, ${videoName[index]}`);
    const file = new Blob([combinedArray.join("\n")], { type: "text/plain" });    
    element.href = URL.createObjectURL(file);
    element.download = "IDSUBMIT.txt";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <div className="border-2 fixed top-25 right-28 bg-white rounded-lg shadow-lg z-50 w-56">
      <div className="bg-slate-200 rounded-t-lg py-2 px-6 flex justify-between border-b-2">
        <button className="text-sky-500	transition-all hover:text-sky-900">
          <FaFileDownload size={20} onClick={DownloadID} />
        </button>
        <button
          className="text-red-500 transition-all hover:text-red-900"
          onClick={() => ClearID("all")}
        >
          <MdDeleteOutline size={25} />
        </button>
      </div>
      {listId.length > 0 ? (
        <div className="max-h-96 overflow-y-auto pl-4 ">
          {listId.map((item, idx) => (
            <div className="flex justify-between p-3 pr-6 border-b last:border-none">
              <span key={idx}>
                {videoName[idx]}, {item}
              </span>
              <button
                className="text-red-500 transition-all hover:text-red-900"
                onClick={() => ClearID(item)}
              >
                <MdDeleteOutline size={20} />
              </button>
            </div>
          ))}
        </div>
      ) : (
        <div className="h-10"></div>
      )}
    </div>
  );
};

export default IdListSubmit;
