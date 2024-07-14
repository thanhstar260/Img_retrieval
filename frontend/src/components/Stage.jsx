import React, { useCallback, useState } from 'react'
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
        type: "object",
        name: "Object",
        icon: <FaRegObjectUngroup />

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
    }

]

// description:
// the format of 'data' will be like below:
// {
//      type: String
//      data: Object <depend on different type>
//      lang: String      
// }


const Stage = ({id, canClose, onClose, onChange}) => {
    const [selected, setSelected] = useState("scene");
    const [lang, setLang] = useState("vie");
    const [data, setData] = useState({
        type: "scene",
        data: undefined,
        lang: 'vie'
    });

    const selectInputTypeHandler = (type) => {
        if(type === selected)
            return;
        setSelected(type);
        setData({
            ...data,
            type: selected,
            data: undefined,
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


    const getSearchControl = useCallback(() => {
        {
            switch(selected) {
                case "scene":
                    return <TextSearchControl id={id} label={"Enter the scene description"}/>
                case "image":
                    return <ImageSearchControl id={id} />;
                case "text":
                    return <TextSearchControl />;
                case "object":
                    return;
                case "speech":
                    return;
                case "sketch":
                    return;
            }
        }
    }, [selected])

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
                onClick={() => selectInputTypeHandler(type.type)}>
                {type.icon}
            </IconButton>)}
        </div>

        {
                getSearchControl(selected)
        }
        <div className='flex items-center text-teal-500 mt-4'>
            <IoLanguageSharp className='text-lg mr-2' name={id}/>
            <span className='mr-4'>Language: </span>
            <LangRadioGroup value={lang} onChange={selectLangHandler}/>
        </div>
    </div>
  )
}


export default Stage