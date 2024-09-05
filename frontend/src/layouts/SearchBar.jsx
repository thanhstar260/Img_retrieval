import React, { useEffect, useRef, useState } from 'react'
import IconButton from '../components/IconButton';
import Stage from '../components/Stage';
import { v4 as uuidv4 } from 'uuid';
import { IoIosAdd } from "react-icons/io";
import OutlineButton from '../components/OutlineButton';
import { PiRankingLight } from "react-icons/pi";
import { IoIosSearch } from "react-icons/io";
import { twMerge } from 'tailwind-merge';
import { GoArrowLeft } from "react-icons/go";
import QABox from '../components/QABox';

const SearchBar = ({onSubmit, isSubmitting, K, onChangeK, onRerank, open, setOpen}) => {
    const [canClose, setCanClose] = useState(false);
    const [stages, setStages] = useState({
        [uuidv4()]: {
            data: {},
            lang: "eng"
        }
    });

    useEffect(() => {
        if(Object.keys(stages).length > 1) {
            setCanClose(true);
        } else {
            setCanClose(false);
        }

        document
            .querySelectorAll(".stage-name")
            .forEach((value, key) => {
                value.innerHTML = key + 1;
            })
    }, [Object.keys(stages)])
    
    const addNewStageHandler = () => {
        setStages({
            ...stages,
            [uuidv4()]: {
                data: {},
                lang: "eng",
            }
            })
        } 

    const closeStageHandler = (key) => {
        delete stages[key];
        setStages({...stages})
    }

    const changeDataInStage = (key) => {
        return (newValue) => {
            setStages(
                {
                    ...stages,
                    [key]: newValue
                }
            )
        }
    }

  return (
    <div className={twMerge(
        'w-[24rem] bg-slate-100 h-screen px-4 py-8 overflow-y-scroll shrink-0 sticky top-0 transition-all',
        `${isSubmitting ? 'cursor-wait' : ''}`,
        `${!open ? ' -translate-x-full w-0' : ''}`
    )}>
        <div className='mb-6'>
            <label className='text-teal-500 m-3'>K: </label>
            <input type='number' className='ring-2 ring-slate-300 rounded-md max-w-20 focus:outline-none focus:ring-teal-500 transition-all px-2 py-0.25 text-slate-600' value={K} min={1} step={1} onChange={(e)=>{onChangeK(e.target.value)}}/>
        </div>
        <IconButton 
            label="Close"
            className="border-2 border-teal-500 hover:bg-teal-500 hover:text-white mx-auto mt-4 absolute right-4 top-1"
            onClick={() => setOpen(false)}
        >
             <GoArrowLeft className='text-2xl'/>
        </IconButton>
        <QABox className="mb-6"/>
        <div className='flex flex-col gap-4'>
        {
            Object.keys(stages).map(key => <Stage key={key} canClose={canClose} id={key} onClose={() => closeStageHandler(key)} onChange={changeDataInStage(key)}></Stage>)
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
            <OutlineButton onClick={onRerank}>
                <PiRankingLight className='inline-block text-xl'/> Rerank
            </OutlineButton>
            <OutlineButton onClick={() => {
                onSubmit(stages)
            }}>
                <IoIosSearch className='inline-block text-xl'/> Search
            </OutlineButton>
        </div>
    </div>
  )
}

export default SearchBar;