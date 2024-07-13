import React, { useEffect, useState } from 'react'
import IconButton from '../components/IconButton';
import Stage from '../components/Stage';
import { v4 as uuidv4 } from 'uuid';
import { IoIosAdd } from "react-icons/io";

const SearchBar = () => {
    const [stages, setStages] = useState([{
        key: uuidv4(),
        stage: <Stage id={uuidv4()}></Stage>
    }]);

    useEffect(() => {
        document
            .querySelectorAll(".stage-name")
            .forEach((value, key) => {
                value.innerHTML = key + 1;
            })
    }, [stages])
    
    const addNewStageHandler = () => {
        setStages([
            ...stages,
            {
                key: uuidv4(),
                stage: <Stage id={uuidv4()}/>
            }
        ])
    }

  return (
    <div className='w-80 bg-slate-100 h-screen px-6 py-8 overflow-scroll'>
        <div className='flex flex-col gap-4'>
        {
            stages.map(elm => elm.stage)
        }
        </div>
        <IconButton 
            label="Add new stage"
            className="border-2 border-teal-500 hover:bg-teal-500 hover:text-white mx-auto mt-4"
            onClick={addNewStageHandler}
        >
             <IoIosAdd className='text-2xl'/>
        </IconButton>
    </div>
  )
}

export default SearchBar;