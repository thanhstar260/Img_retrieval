import React, { useEffect, useState } from 'react'
import IconButton from '../components/IconButton';
import Stage from '../components/Stage';
import { v4 as uuidv4 } from 'uuid';
import { IoIosAdd } from "react-icons/io";
import OutlineButton from '../components/OutlineButton';
import { PiRankingLight } from "react-icons/pi";
import { IoIosSearch } from "react-icons/io";

const SearchBar = () => {
    const [canClose, setCanClose] = useState(false);
    const [stages, setStages] = useState([{
        key: uuidv4(),
    }]);

    useEffect(() => {
        if(stages.length > 1) {
            setCanClose(true);
        } else {
            setCanClose(false);
        }

        document
            .querySelectorAll(".stage-name")
            .forEach((value, key) => {
                value.innerHTML = key + 1;
            })
    }, [stages])
    
    const addNewStageHandler = () => {
        setStages([
            ...stages,
            uuidv4(),
        ])
    }

    const closeStageHandler = (key) => {
        setStages(
            stages.filter((ele => ele !== key))
        )
    }

  return (
    <div className='w-80 bg-slate-100 h-screen px-6 py-8 overflow-scroll'>
        <div className='flex flex-col gap-4'>
        {
            stages.map(elm => <Stage key={elm} canClose={canClose} id={elm} onClose={() => closeStageHandler(elm)}></Stage>)
        }
        </div>
        <IconButton 
            label="Add new stage"
            className="border-2 border-teal-500 hover:bg-teal-500 hover:text-white mx-auto mt-4"
            onClick={addNewStageHandler}
        >
             <IoIosAdd className='text-2xl'/>
        </IconButton>

        <div className='flex justify-around mt-8'>
            <OutlineButton>
                <PiRankingLight className='inline-block text-xl'/> Rerank
            </OutlineButton>
            <OutlineButton>
                <IoIosSearch className='inline-block text-xl'/> Search
            </OutlineButton>
        </div>
    </div>
  )
}

export default SearchBar;