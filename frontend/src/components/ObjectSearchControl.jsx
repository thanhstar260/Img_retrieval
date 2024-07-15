import React, { useEffect, useMemo, useRef, useState } from 'react'
import SelectMenu from './SelectMenu'
import { twMerge } from 'tailwind-merge'
import IconButton from './IconButton'
import BrushSizeSlider from './BrushSizeSlider'
import Canvas from './Canvas'
import SelectedObject from './SelectedObject'

const objectTypes = [
    {
        id: 1,
        name: 'Human'
    },
    {
        id: 2,
        name: 'Dog'
    },
    {
        id: 3,
        name: 'Cat',
    },
    {
        id: 4,
        name: 'Book'
    },
    {
        id: 5,
        name: 'Table'
    },
    {
        id: 6,
        name: 'Car'
    }
]

const colors = [
    {
        name: 'lime',
        hex: '#00FF00',
    },
    {
        name: 'gray',
        hex: '#808080',
        rgb: 'rgb(128, 128, 128)'
    },
    {
        name: 'red',
        hex: '#FF0000',
        rgb: 'rgb(255, 0, 0)'
    },
    {
        name: 'yellow',
        hex: '#FFFF00',
        rgb: 'rgb(255, 255, 0)'
    },
    {
        name: 'aqua',
        hex: '#00FFFF',
        rgb: 'rgb(0, 255, 255)'
    },
    {
        name: 'teal',
        hex: '#008080',
        rgb: 'rgb(0, 128, 128)'
    },
    {
        name: 'blue',
        hex: '#0000FF',
        rgb: 'rgb(0, 0, 255)'
    },
    {
        name: 'navy',
        hex: '#000080',
        rgb: 'rgb(0, 0, 128)'
    },
    {
        name: 'fuchsia',
        hex: '#FF00FF',
        rgb: 'rgb(255, 0, 255)'
    },
    {
        name: 'purple',
        hex: '#800080',
        rgb: 'rgb(128, 0, 128)'
    }
]

const getObjectById = (id) => {
    return objectTypes.find((obj) => obj.id === id)
}

const ObjectSearchControl = () => {
    const [selectedObj, setSelectedObj] = useState(1);

    const [selectedColor, setSelectedColor] = useState("white");

    const [brushSize, setBrushSize] = useState(2);

    const [collection, setCollection] = useState({});

    const handleSelectColor = (color) => {
        for(let key in collection) {
            if(key !== getObjectById(selectedObj).name && collection[key] === color.name) {
                alert("This color was used for another object, please choose another one");
                return
            } 
        }

        const name = getObjectById(selectedObj).name

        setCollection({
            ...collection,
        [name]: color.name
        });
        
        setSelectedColor(color.name);
    }

    const handleOnClose = (name) => {
        const newCollection = {
            ...collection
        }

        delete newCollection[name]
        setCollection(newCollection)
    }


  return (
    <div>
        <div>
            <label className=' text-teal-500 mr-4 text-sm'>Object</label>
            <SelectMenu className='max-w-44' options={objectTypes} selected={selectedObj} onSelect={setSelectedObj}/>
        </div>
        <div className='flex mt-2 h-12 items-center'>
            <span className='text-teal-500 mr-4 text-sm'>Color</span>
            <div className='flex gap-3 overflow-x-scroll h-full items-center z-10'>
            
                {colors.map(color => {
                    return (
                        <IconButton
                            key={color.name} 
                            className={`p-0 hover:shadow-lg hover:scale-105 ${selectedColor === color.name ? 'ring-4 ring-teal-400' : ''}`}
                            onClick={() => handleSelectColor(color)}>
                            <div className={
                                twMerge(
                                    "size-6 rounded-full shrink-0 p-1",
                                    
                                )
                            }
                            style={{backgroundColor: color.hex}}></div>
                        </IconButton>
                    )
                })}
            </div>
        </div>
        <div className='flex items-center mt-2'>
            <span className='mr-4 text-teal-500 text-sm'>Brush</span>
            <BrushSizeSlider className={'w-40'} value={brushSize} onChange={(e) => setBrushSize(e.target.value)}/>
        </div>
        <Canvas type={"rectangle"} color={selectedColor} brushSize={brushSize}/>

        <div className='mt-4 flex items-center h-7'>
            <p className='text-sm text-teal-500 mr-4'>Collection</p>
            <div className='flex gap-2 overflow-y-hidden'>
                {Object
                    .keys(collection)
                    .reverse()
                    .map(name => 
                        <SelectedObject 
                            name={name} 
                            color={collection[name]} 
                            onRemove={() => handleOnClose(name)}
                        />)}
            </div>
        </div>
    </div>
  )
}

export default ObjectSearchControl