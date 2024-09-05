import React, { useEffect, useRef, useState } from 'react'

const Canvas = ({color, value,  brushSize, type, onStopDraw, onUndo, onDelete}) => {
    const canvasRef = useRef(null);

    const [isDrawing, setIsDrawing] = useState(false);
    const [prevCoordinate, setPreCoordinate] = useState({
        offsetX: null,
        offsetY: null
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
    }, [history])

    const saveCanvasState = (snapshot) => {
        setHistory((prevHis) => {
            return [
                ...prevHis,
                snapshot
            ]
        })
    }


    const handleUndo = () => {
        if(history.length > 0) {
            contextRef.current.putImageData(history[history.length - 1], 0, 0)
            if(type === "rectangle") {
                onUndo();
            } else if(history.length > 1) {
                onStopDraw(canvasRef.current.toDataURL("image/jpeg"));
            } else {
                onStopDraw(null);
            }
        }
        setHistory((prevHistory) => {
            const newHistory = [...prevHistory]
            newHistory.pop();
            return newHistory;
        })
    }

    const drawRectangle = (e) => {
        if(color == "white")
            return;
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
        if(color == "white")
            return;
        if (isDrawing) {
            contextRef.current.lineTo(
                e.nativeEvent.offsetX,
                e.nativeEvent.offsetY
            );
            contextRef.current.stroke();
        }
    }

    const startDrawing = (e) => {
        if(color == "white")
            return;
        setPreCoordinate({
            offsetX: e.nativeEvent.offsetX,
            offsetY: e.nativeEvent.offsetY
        })
        contextRef.current.beginPath();
        contextRef.current.moveTo(
            e.nativeEvent.offsetX, e.nativeEvent.offsetY
        )
        setIsDrawing(true);
        const snapshot = contextRef.current.getImageData(0, 0, canvasRef.current.width, canvasRef.current.height)
        setSnapshot(snapshot)
        saveCanvasState(snapshot)
    }

    const stopDrawing = (e) => {
        if(color == "white")
            return;        

        setIsDrawing(false);
        contextRef.current.closePath();
        if(type == "rectangle" && color != "white") {
            const currentOffset = {
                x: e.nativeEvent.offsetX,
                y: e.nativeEvent.offsetY
            }

            const coordinate = prevCoordinate.offsetX < currentOffset.x ?
            [   prevCoordinate. offsetX, 
                prevCoordinate.offsetY, 
                currentOffset.x, currentOffset.y
            ] : 
            [   currentOffset.x,
                currentOffset.y,
                prevCoordinate.offsetX,
                prevCoordinate.offsetY
            ]


            onStopDraw(coordinate)
        } else {
            onStopDraw(canvasRef.current.toDataURL("image/jpeg"))
        }
        
    }

    useEffect(() => {
        const canvas = canvasRef.current;

        const context = canvas.getContext('2d');
        context.lineCap = "round";
        context.lineWidth = brushSize
        context.strokeStyle = color
        contextRef.current = context
        
    }, [brushSize, color])

    useEffect(() => {
        if(!value) {
            setHistory([]);
            contextRef.current.fillStyle = "white"
            contextRef.current.fillRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        }
    }, [value])

  return (
    <canvas 
            ref={canvasRef} 
            className='aspect-video  bg-white ring-2 ring-slate-300 mt-4 cursor-crosshair'
            onMouseDown={startDrawing}
            onMouseMove={type === 'rectangle' ? drawRectangle : handleDrawing}
            onMouseUp={stopDrawing}>
    </canvas>
  )
}

export default Canvas