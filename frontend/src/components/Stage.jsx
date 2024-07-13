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


const Stage = ({id, canClose}) => {
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
    }

    const selectLangHandler = (event) => {
        setLang(event.target.value);
        setData({
            ...data,
            lang: lang
        })
    }

    const getSearchControl = useCallback(() => {
        {
            switch(selected) {
                case "scene":
                    return <TextSearchControl id={id} label={"Enter the scene description"}/>
                case "image":
                    return;
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
    <div className='px-4 py-4 bg-slate-50 rounded-lg'>
        <p className='text-teal-500 mb-2'>Stage <span className='stage-name'></span></p>
        <div
         className='flex flex-row gap-x-2 mb-4'>
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