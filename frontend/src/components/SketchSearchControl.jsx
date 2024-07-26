import React, { useState } from 'react'
import BrushSizeSlider from './BrushSizeSlider';
import Canvas from './Canvas';

const SketchSearchControl = ({data, onChange}) => {

    const [brushSize, setBrushSize] = useState(2);

    const handleChangeData = (image) => {
      console.log(image)
      onChange("sketch", image);
    }

  return (
    <div>
        <p className='text-sm text-teal-500'>Sketch a picture</p>
        <div className='flex items-center mt-2'>
            <span className='mr-4 text-teal-500 text-sm'>Brush</span>
            <BrushSizeSlider className={'w-40'} value={brushSize} onChange={(e) => setBrushSize(e.target.value)}/>
        </div>
        <div className='w-full flex justify-center'>
        <Canvas type={"drawing"} color="black" brushSize={brushSize} value={data} onStopDraw={handleChangeData}/>
        </div>
    </div>
  )
}

export default SketchSearchControl