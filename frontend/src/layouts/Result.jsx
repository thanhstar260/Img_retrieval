import { SlReload } from "react-icons/sl";
import { GoHome } from "react-icons/go";
import { GrNotes } from "react-icons/gr";
import { RiSendPlane2Fill } from "react-icons/ri";
import { IoMdSearch } from "react-icons/io";
import ListImageResult from "../components/ListImageResult";
import { useState } from "react";

const Result = () => {
  const [reloadCount, setReloadCount] = useState(0);
  const btn_style =
  "text-teal-500 px-2 py-2 rounded-full transition-all hover:text-white hover:bg-teal-500";

  const handleReload = () => {
    setReloadCount((prevCount) => prevCount + 1);
  };


  return (
    <div className="px-6 py-8 flex-grow w-3/5 h-full">
      <div className="flex flex-row gap-44 mb-5">
        <div className="flex gap-12">
          <button className={btn_style}>
            <SlReload size={35} />
          </button>
          <button className={btn_style}>
            <GoHome size={35} onClick={handleReload}/>
          </button>
        </div>
        <div className="flex flex-row items-center border rounded-full px-3 border-teal-500 w-full">
          <input type="text" className="outline-none px-4 w-full " />
          <button className="hover:text-teal-500">
            <IoMdSearch size={25}/>
          </button>
        </div>
        <div className="flex gap-12">
          <button className={btn_style}>
            <GrNotes size={35} />
          </button>
          <button className={btn_style}>
            <RiSendPlane2Fill size={35} />
          </button>
        </div>
      </div>

      {/*Two-dimensional array [stage][idx] -> idImg*/}
      <ListImageResult key={reloadCount} ImageIdArr={[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26],[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]]} />

    </div>
  );
};
export default Result;
