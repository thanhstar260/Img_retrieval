import React, { useCallback, useEffect, useState } from 'react'
import { MdMovieEdit } from "react-icons/md";
import { CiImageOn } from "react-icons/ci";
import { MdOutlineTextFields } from "react-icons/md";
import { MdOutlineKeyboardVoice } from "react-icons/md";
import { RiSketching } from "react-icons/ri";
import { FaRegObjectUngroup } from "react-icons/fa";
import IconButton from './IconButton';
import TextSearchControl from './TextSearchControl';
import { IoLanguageSharp } from "react-icons/io5";
import LangRadioGroup from './LangRadioGroup';
import { IoIosClose } from "react-icons/io";
import ImageSearchControl from './ImageSearchControl';
import ObjectSearchControl from './ObjectSearchControl';
import SketchSearchControl from './SketchSearchControl';

const inputTypes = [
    {
        type: "scene",
        name: "Scene description",
        icon: <MdMovieEdit />
    },
    {
        type: "image",
        name: "Image",
        icon: <CiImageOn />
    },
    {
        type: "text",
        name: "Text on screen",
        icon: <MdOutlineTextFields />
    },
    {
        type: "speech",
        name: "Speech",
        icon: <MdOutlineKeyboardVoice />
    },
    {
        type: "sketch",
        name: "Sketch",
        icon: <RiSketching />
    },
    {
        type: "object",
        name: "Object",
        icon: <FaRegObjectUngroup />

    },

]

// description:
// the format of 'data' will be like below:
// {
//      type: String
//      data: Object <depend on different type>
//      lang: String      
// }


const Stage = ({id, canClose, onClose, onChange, onStopDraw}) => {
    const [selected, setSelected] = useState("scene");
    const [lang, setLang] = useState("eng");
    const [data, setData] = useState({
        data:  
        {    
            scene: undefined,
            image: undefined,
            text: undefined,
            speech: undefined,
            sketch: undefined,
            object: undefined,
        },
        lang: 'eng'
    });

    const selectInputTypeHandler = (type) => {
        if(type === selected)
            return;
        setSelected(type);
        setData({
            ...data,
            lang: lang
        })
        onChange(data);
    }


    const selectLangHandler = (event) => {
        setLang(event.target.value);
        setData({
            ...data,
            lang: lang
        })
        onChange(data);
    }

    const handleChangeData = (type, newSearchData) => {
        console.log(data)
        console.log(newSearchData)
        const newData = {
            ...data
        }
        newData.data[type] = newSearchData;
        setData(newData);
    }

    useEffect(() => {
        if(data) {

        }
    })

  return (
    <div className='relative px-4 py-4 bg-slate-50 rounded-lg'>
        {canClose && 
            <IconButton onClick={onClose} label="Close" className='absolute top-3 right-4 text-gray-600 hover:text-red-500'>
            <IoIosClose />
        </IconButton>}
        <p className='text-teal-500 mb-4'>Stage <span className='stage-name'></span></p>
        <div
         className='flex flex-row justify-between mb-4'>
            {inputTypes.map(type => <IconButton 
                key={type.name} 
                label={type.name}
                isSelected={selected === type.type}
                onClick={() => selectInputTypeHandler(type.type)}
                className={`${data.data[type.type] && selected !== type.type ? 'bg-violet-400 text-white' : ''}`}>
                {type.icon}
            </IconButton>)}
        </div>
        <div className={`${selected === 'scene' ? 'block' : 'hidden'}`}>
            <TextSearchControl id="scene" label={"Enter the scene description"} data={data.data["scene"]} onChange={handleChangeData}/>
        </div>
        <div className={`${selected === 'image' ? 'block' : 'hidden'}`}>
            <ImageSearchControl id="image" data={data.data["image"]} onChange={handleChangeData}/>
        </div>
        <div className={`${selected === 'text' ? 'block' : 'hidden'}`}>
            <TextSearchControl id="text" label={"Enter your text"} data={data.data["text"]} onChange={handleChangeData}/>
        </div>
        <div className={`${selected === 'speech' ? 'block' : 'hidden'}`}>
            <TextSearchControl id="speech" label={"Enter your text"} data={data.data["speech"]} onChange={handleChangeData}/>   
        </div>
        <div className={`${selected === 'sketch' ? 'block' : 'hidden'}`}>
                <SketchSearchControl data={data.data["sketch"]} onChange={handleChangeData}/>  
        </div>
        <div className={`${selected === 'object' ? 'block' : 'hidden'}`}>
                <ObjectSearchControl data={data.data["object"]} onChange={handleChangeData}/>  
        </div>
        <div className='flex items-center text-teal-500 mt-4'>
            <IoLanguageSharp className='text-lg mr-2' name={id}/>
            <span className='mr-4'>Language: </span>
            <LangRadioGroup value={lang} onChange={selectLangHandler}/>
        </div>
    </div>
  )
}


export default Stage