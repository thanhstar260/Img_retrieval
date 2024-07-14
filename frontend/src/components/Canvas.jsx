import React, { useEffect, useRef, useState } from 'react'

const Canvas = ({color, brushSize, type}) => {
    const canvasRef = useRef(null);

    const [isDrawing, setIsDrawing] = useState(false);
    const [prevCoordinate, setPreCoordinate] = useState({
        offsetX: undefined,
        offsetY: undefined
    })
    const [snapshot, setSnapshot] = useState('');

    const contextRef = useRef(null);

    const [history, setHistory] = useState([]);

    useEffect(() => {
        const handleKeyDown = (e) => {
            if(e.ctrlKey && e.key === 'z') {
                handleUndo();
            }
        }

        document.addEventListener('keydown', handleKeyDown)

        return () => {
            document.removeEventListener('keydown', handleKeyDown)
        }
    }, [])

    const saveCanvasState = () => {
        const canvas = canvasRef.current;
        setHistory([
            ...history,
            contextRef.current.getImageData(0, 0, canvas.width, canvas.height)
        ])
    }

    const restoreCanvas = () => {
        const canvas = canvasRef.current;
        if(history.length > 0) {
            contextRef.current.putImageData(history[history.length - 1], 0, 0)
        } else {
            contextRef.current.clearRect(0, 0, canvas.width, canvas.height)
        }
    }

    const handleUndo = () => {
        setHistory((prevHistory) => {
            const newHistory = [...prevHistory]
            newHistory.pop();
            return newHistory;
        })
        restoreCanvas();
    }

    const drawRectangle = (e) => {
        if (isDrawing) {
            contextRef.current.putImageData(snapshot, 0, 0);
            contextRef.current.strokeRect(
                e.nativeEvent.offsetX, 
                e.nativeEvent.offsetY, 
                prevCoordinate.offsetX - e.nativeEvent.offsetX, 
                prevCoordinate.offsetY - e.nativeEvent.offsetY)
        }
    } 

    const handleDrawing = (e) => {
        if (isDrawing) {
            contextRef.current.lineTo(
                e.nativeEvent.offsetX,
                e.nativeEvent.offsetY
            );
            contextRef.current.stroke();
        }
    }

    const startDrawing = (e) => {
        setPreCoordinate({
            offsetX: e.nativeEvent.offsetX,
            offsetY: e.nativeEvent.offsetY
        })
        contextRef.current.beginPath();
        contextRef.current.moveTo(
            e.nativeEvent.offsetX, e.nativeEvent.offsetY
        )
        setIsDrawing(true);
        setSnapshot(contextRef.current.getImageData(0, 0, canvasRef.current.width, canvasRef.current.height))
    }

    const stopDrawing = (e) => {
        setIsDrawing(false);
        contextRef.current.closePath();
        saveCanvasState();
    }

    useEffect(() => {
        const canvas = canvasRef.current;

        const context = canvas.getContext('2d');
        context.lineCap = "round";
        context.lineWidth = brushSize
        context.strokeStyle = color
        contextRef.current = context
        
    }, [brushSize, color])
  return (
    <canvas 
            ref={canvasRef} 
            className='aspect-video  bg-white ring-2 ring-slate-400 mt-4 cursor-crosshair'
            onMouseDown={startDrawing}
            onMouseMove={type === 'rectangle' ? drawRectangle : handleDrawing}
            onMouseUp={stopDrawing}>
    </canvas>
  )
}

export default Canvas