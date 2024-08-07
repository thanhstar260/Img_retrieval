import { SlReload } from "react-icons/sl";
import { GoHome } from "react-icons/go";
import { GrNotes } from "react-icons/gr";
import { RiSendPlane2Fill } from "react-icons/ri";
import { IoMdSearch } from "react-icons/io";
import ListImageResult from "../components/ListImageResult";
import { useState, useEffect } from "react";

const Result = ({ result, onChangeDataRerank, K, onGoBack, onClear }) => {
  const [reloadCount, setReloadCount] = useState(0);
  const [inputValue, setInputValue] = useState();
  const [dis, setDis] = useState([]);
  const [ids, setIds] = useState([]);
  const [K1, setK] = useState(K);
  const [isShowIdlist, setIsShowIdlist] = useState(false);

  useEffect(() => {
    setK(K);
  }, [K]);
  const btn_style =
    "text-teal-500 px-2 py-2 rounded-full transition-all hover:text-white hover:bg-teal-500";

  const handleReload = () => {
    setReloadCount((prevCount) => prevCount + 1);
  };

  useEffect(() => {
    const idsList = [];
    const disList = [];
    for (const key in result) {
      idsList.push(result[key].ids);
      disList.push(result[key].distances);
    }
    setDis(disList);
    setIds(idsList);
    handleReload();
  }, [result]);

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      handleSetIds();
    }
  };
  const handleSetIds = () => {
    if(inputValue === "") return
    const values = inputValue.split(',').map(value => parseInt(value.trim()));
    setIds([values]);
  };
  const handleClear = () => {
    setIsShowIdlist(false);
    setIds([]);
    onClear();
  };
  const ShowIdList = () => {
    setIsShowIdlist(!isShowIdlist);
  };
  return (
    <div className="px-6 py-4 flex-grow h-screen">
      <div className="flex flex-row gap-44 mb-3">
        <div className="flex gap-12">
          <button className={btn_style} onClick={onGoBack}>
            <SlReload size={30} />
          </button>
          <button className={btn_style}>
            <GoHome size={30} onClick={handleClear} />
          </button>
        </div>
        <div className="flex flex-row items-center border rounded-full px-3 border-teal-500 w-full">
          <input
            type="text"
            className="outline-none px-4 w-full "
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyPress}
          />
          <button className="hover:text-teal-500">
            <IoMdSearch size={25} />
          </button>
        </div>
        <div className="flex gap-12">
          <button
            className={
              !isShowIdlist
                ? btn_style
                : "px-2 py-2 rounded-full transition-all text-white bg-teal-500"
            }
          >
            <GrNotes size={30} onClick={ShowIdList} />
          </button>
          <button className={btn_style}>
            <RiSendPlane2Fill size={30} />
          </button>
        </div>
      </div>

      {/*Two-dimensional array [stage][idx] -> idImg*/}
        <ListImageResult
          K={K1}
          onChangeDataRerank={onChangeDataRerank}
          key={reloadCount}
          ImageIdArr={ids}
          dis={dis}
          isShowIdlist={isShowIdlist}
        />
    </div>
  );
};
export default Result;
