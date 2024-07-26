import React, { useEffect, useMemo, useRef, useState } from 'react'
import SelectMenu from './SelectMenu'
import { twMerge } from 'tailwind-merge'
import IconButton from './IconButton'
import BrushSizeSlider from './BrushSizeSlider'
import Canvas from './Canvas'
import SelectedObject from './SelectedObject'

const objectTypes = [
    'person',        'bicycle',       'car',           'motorcycle',
    'airplane',      'bus',           'train',         'truck',
    'boat',          'traffic light', 'fire hydrant',  'stop sign',
    'parking meter', 'bench',         'bird',          'cat',
    'dog',           'horse',         'sheep',         'cow',
    'elephant',      'bear',          'zebra',         'giraffe',
    'backpack',      'umbrella',      'handbag',       'tie',
    'suitcase',      'frisbee',       'skis',          'snowboard',
    'sports ball',   'kite',          'baseball bat',  'baseball glove',
    'skateboard',    'surfboard',     'tennis racket', 'bottle',
    'wine glass',    'cup',           'fork',          'knife',
    'spoon',         'bowl',          'banana',        'apple',
    'sandwich',      'orange',        'broccoli',      'carrot',
    'hot dog',       'pizza',         'donut',         'cake',
    'chair',         'couch',         'potted plant',  'bed',
    'dining table',  'toilet',        'tv',            'laptop',
    'mouse',         'remote',        'keyboard',      'cell phone',
    'microwave',     'oven',          'toaster',       'sink',
    'refrigerator',  'book',          'clock',         'vase',
    'scissors',      'teddy bear',    'hair drier',    'toothbrush'
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


const ObjectSearchControl = ({onChange, data}) => {
    const [selectedObj, setSelectedObj] = useState(objectTypes[0]);

    const [selectedColor, setSelectedColor] = useState("white");

    const [brushSize, setBrushSize] = useState(2);

    const [collection, setCollection] = useState({});
    
    const handleSelect = (obj) => {
        if(collection[obj]) {
            setSelectedColor(collection[obj])
        } else {
            setSelectedColor("white")
        }

        setSelectedObj(obj)
    }

    const handleStopDraw = (newOffset) => {
        if(!data) {
            onChange("object", [{object: selectedObj, offset: newOffset}])
        } else {
            onChange("object", [...data, {object: selectedObj, offset:newOffset}])
        }
    }

    const handleUndo = () => {
        if(data) {
            if(data.length > 0) {
                data.pop();
                onChange("object", [...data]);
            }
        } else {
            onChange("object", null)
        }
    }

    const handleSelectColor = (color) => {
        for(let key in collection) {
            if(key !== selectedObj && collection[key] === color.name) {
                alert("This color was used for another object, please choose another one");
                return
            } else if(Object.keys(collection).includes(selectedObj) && collection[selectedObj] && collection[selectedObj] !== color.name) {
                alert("This object already has a specific color");
                return
            }
        }

        setCollection({
            ...collection,
        [selectedObj]: color.name
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
            <SelectMenu className='max-w-44' options={objectTypes} selected={selectedObj} onSelect={handleSelect}/>
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
        <div className='w-full flex justify-center'>
        <Canvas type={"rectangle"} color={selectedColor} brushSize={brushSize} onStopDraw={handleStopDraw} onUndo={handleUndo} value={data}/>
        </div>

        <div className='mt-4 flex items-center h-7'>
            <p className='text-sm text-teal-500 mr-4'>Collection</p>
            <div className='flex gap-2 overflow-y-hidden'>
                {Object
                    .keys(collection)
                    .reverse()
                    .map(name => 
                        <SelectedObject 
                            key={name}
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