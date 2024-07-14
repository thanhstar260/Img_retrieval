import React, { useState } from 'react'
import SelectMenu from './SelectMenu'

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
        name: 'white',
        hex: '#FFFFFF',
        rgb: 'rgb(255, 255, 255)'
    },
    {
        name: 'silver',
        hex: '#C0C0C0',
        rgb: 'rgb(192, 192, 192)'
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
        name: 'maroon',
        hex: '#800000',
        rgb: 'rgb(128, 0, 0)'
    },
    {
        name: 'yellow',
        hex: '#FFFF00',
        rgb: 'rgb(255, 255, 0)'
    },
    {
        name: 'olive',
        hex: '#808000',
        rgb: 'rgb(128, 128, 0)'
    },
    {
        name: 'lime',
        hex: '#00FF00',
        rgb: 'rgb(0, 255, 0)'
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

  return (
    <div>
        <div>
            <label className=' text-teal-500 mr-3'>Object</label>
            <SelectMenu options={objectTypes} selected={selectedObj} onSelect={setSelectedObj}/>
        </div>
    </div>
  )
}

export default ObjectSearchControl