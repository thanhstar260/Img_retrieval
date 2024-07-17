import React, { useEffect, useRef, useState } from 'react'
import IconButton from './IconButton'
import { BiImageAdd } from "react-icons/bi";
import { twMerge } from 'tailwind-merge';

const ImageSearchControl = ({id, data, onChange}) => {
    const fileRef = useRef(null);

    const changeImageUrlHandler = (event) => {
        const val = event.target.value;
        var url;
        try {
            url = new URL(val);
        } catch(e) {
            url = null;
        }
        if(url) {
            onChange(id, data);
        }
    }

    const selectImageHandler = (event) => {
        if(fileRef) {
            fileRef.current.click();
        }
    }

    const coverFileToURL = (blob) => {
        var reader = new FileReader();
                    reader.onload = function (event) {
                        onChange(id, event.target.result);
                    }; 
                    reader.readAsDataURL(blob);
    }

    const pasteImageUrlHandler = (event) => {
        const file = event.clipboardData.files[0];
        if(file && file.type.startsWith("image")) {
            var items = event.clipboardData.items;
            for (var index in items) {
                var item = items[index];
                if (item.kind === 'file') {
                    var blob = item.getAsFile();
                    coverFileToURL(blob)
                }
            }
        }
    }

    const changeFileHandler = (event) => {
        const file = event.target.files[0];
        coverFileToURL(file)
    }
    
    return (
    <div>
        <label className='text-sm text-teal-500 mb-2 inline-block' htmlFor={id}
        >Paste or drop an image</label>
        <input 
            className='px-2 py-1 rounded-lg w-full ring-2 ring-slate-300 mb-3 focus:outline-none
            focus:ring-teal-500'
            placeholder='Image URL'
            onChange={changeImageUrlHandler}
            onPaste={pasteImageUrlHandler}>
        </input>
        <div id={id} className="
        w-full h-[10rem] border-dashed border-teal-500 border-2 rounded-lg group transition-all relative overflow-hidden">
            <input type='file' className='hidden' ref={fileRef} accept='image/png,image.jpeg' onChange={changeFileHandler}></input>
            {data && <img src={data} className=' object-contain object-center w-full h-full border-none border-0' style={{border:'0'}}/>}
            <IconButton onClick={selectImageHandler} className={
                twMerge(
                    "right-1/2 translate-x-1/2 top-1/2 -translate-y-1/2  bg-white absolute",
                    data ? 'group-hover:block hidden' : ''
                )
            }>
                <BiImageAdd className='text-3xl'/>
            </IconButton>
        </div>
    </div>
  )
}

export default ImageSearchControl