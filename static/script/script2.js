// Các hằng số màu sắc cho các điểm keypoint
const COLORS = [
    "#E92EFB", "#FF2079", "#FF2079", "#FE6F61", "#FE6F61",
    "#FEEC2D", "#FEEC2D", "#00FF2E", "#00FF2E", "#00DDFF",
    "#00DDFF", "#057DFF", "#057DFF", "#E92EFB"
];

const Keypoint_names = [
    "Nose", "Left Shoulder", 
    "Right Shoulder", "Left Elbow", "Right Elbow", "Left Wrist", "Right Wrist", 
    "Left Hip", "Right Hip", "Left Knee", "Right Knee", "Left Ankle", "Right Ankle", "Neck"
]

// Các điểm keypoint mặc định
const DEFAULT_POINTS = [
    { id: 0, cx: 160, cy: 30 },
    { id: 1, cx: 132, cy: 60 },
    { id: 2, cx: 188, cy: 60 },
    { id: 3, cx: 108, cy: 98 },
    { id: 4, cx: 216, cy: 106 },
    { id: 5, cx: 112, cy: 164 },
    { id: 6, cx: 208, cy: 164 },
    { id: 7, cx: 144, cy: 154 },
    { id: 8, cx: 184, cy: 154 },
    { id: 9, cx: 126, cy: 230 },
    { id: 10, cx: 196, cy: 230 },
    { id: 11, cx: 122, cy: 300 },
    { id: 12, cx: 200, cy: 300 },
    { id: 13, cx: 160, cy: 60 }
];

// Hàm vẽ các đường nối giữa các điểm keypoint
function drawLines(svg, points) {
    // Xóa các đường nối cũ
    const existingLines = svg.querySelectorAll("line");
    existingLines.forEach(line => line.remove());

    const lineConnections = [
        [0, 13], [13, 1], [13, 2], [7, 8], [1, 7], [2, 8], [7, 9],
        [9, 11], [8, 10], [10, 12], [1, 3], [3, 5], [2, 4], [4, 6]
    ];
    lineConnections.forEach(connection => {
        const [startId, endId] = connection;
        const startPoint = points.find(p => p.id === startId);
        const endPoint = points.find(p => p.id === endId);
        if (startPoint && endPoint) {
            const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
            line.setAttribute("x1", startPoint.cx);
            line.setAttribute("y1", startPoint.cy);
            line.setAttribute("x2", endPoint.cx);
            line.setAttribute("y2", endPoint.cy);
            line.setAttribute("stroke", "blue");
            line.setAttribute("stroke-width", "5");
            svg.appendChild(line);
        }
    });
}

let currentPoints = [];

function setPoints(newPoints) {
    // Cập nhật các điểm keypoint
    for (let i = 0; i < newPoints.length; i++) {
        points[i].cx = newPoints[i].cx;
        points[i].cy = newPoints[i].cy;
    }
}

function movePoint(id, newCx, newCy) {
    // Tìm điểm cần di chuyển trong currentPoints và cập nhật tọa độ mới
    for (let point of currentPoints) {
        if (point.id === id) {
            point.cx = newCx;
            point.cy = newCy;
            break;
        }
    }

    // Cập nhật các điểm trên SVG
    setPoints(currentPoints);
}

// // Hàm thay đổi tọa độ các điểm keypoint
// function normalizePoints(points, svg) {
//     const svgRect = svg.getBoundingClientRect();
//     return points.map(point => {
//         const cx = parseFloat((point.cx / svgRect.width).toFixed(4));
//         const cy = parseFloat((point.cy / svgRect.height).toFixed(4));
//         return { ...point, cx, cy };
//     });
// }

// Hàm vẽ các điểm keypoint và xử lý sự kiện
function drawPoints(svg, points, setPoints) {
    points.forEach(point => {
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", point.cx);
        circle.setAttribute("cy", point.cy);
        circle.setAttribute("r", "7");
        circle.setAttribute("fill", COLORS[point.id]);
        circle.setAttribute("class", "cursor-grab");

        let isDragging = false;

        // Sự kiện bắt đầu kéo điểm
        circle.addEventListener("mousedown", function(e) {
            isDragging = true;
            const rect = svg.getBoundingClientRect();
            const offsetX = e.clientX - rect.left;
            const offsetY = e.clientY - rect.top;

            // Sự kiện di chuyển điểm
            document.addEventListener("mousemove", moveHandler);

            // Sự kiện kết thúc kéo điểm
            document.addEventListener("mouseup", function() {
                isDragging = false;
                document.removeEventListener("mousemove", moveHandler);
            });

            function moveHandler(e) {
                if (isDragging) {
                    const newX = e.clientX - rect.left;
                    const newY = e.clientY - rect.top;
                    const newPoints = points.map(p => {
                        if (p.id === point.id) {
                            return { ...p, cx: newX, cy: newY };
                        }
                        return p;
                    });
                    setPoints(newPoints);
                    drawLines(svg, newPoints);
                    updateKeypoints(svg, newPoints); // Cập nhật vị trí các điểm keypoints trên SVG
                    updateKeypointsTextarea(newPoints);
                    updateInpKeypointsTextarea(svg, newPoints)
                }
            }
        });
        updateKeypointsTextarea(points);
        updateInpKeypointsTextarea(svg, points)
        svg.appendChild(circle);
    });
    
}

// Hàm cập nhật vị trí của các điểm keypoints trên SVG
function updateKeypoints(svg, points) {
    const circles = svg.querySelectorAll("circle");
    circles.forEach((circle, index) => {
        circle.setAttribute("cx", points[index].cx);
        circle.setAttribute("cy", points[index].cy);
    });
}

// Hàm xóa điểm keypoints và các đường nối cũ
function clearPose(svg) {
    const existingCircles = svg.querySelectorAll("circle");
    existingCircles.forEach(circle => circle.remove());

    const existingLines = svg.querySelectorAll("line");
    existingLines.forEach(line => line.remove());
}

// Hàm thay đổi tọa độ các điểm keypoint cho tư thế Hands Folded
function setArmsFolded(svg, setPoints) {
    const newPoints = [
        { id: 0, cx: 160, cy: 30 },
        { id: 1, cx: 130, cy: 72 },
        { id: 2, cx: 194, cy: 68 },
        { id: 3, cx: 120, cy: 128 },
        { id: 4, cx: 208, cy: 122 },
        { id: 5, cx: 184, cy: 120 },
        { id: 6, cx: 146, cy: 132 },
        { id: 7, cx: 136, cy: 154 },
        { id: 8, cx: 184, cy: 154 },
        { id: 9, cx: 120, cy: 230 },
        { id: 10, cx: 200, cy: 230 },
        { id: 11, cx: 118, cy: 300 },
        { id: 12, cx: 202, cy: 300 },
        { id: 13, cx: 160, cy: 60 }
    ];
    setPoints(newPoints);
    drawLines(svg, newPoints);
    updateKeypoints(svg, newPoints); // Cập nhật vị trí các điểm keypoints trên SVG
    updateKeypointsTextarea(newPoints);
    updateInpKeypointsTextarea(svg, newPoints)
}

// Hàm thay đổi tọa độ các điểm keypoint cho tư thế Upside Down
function setUpSideDown(svg, setPoints) {
    const newPoints = [
        { id: 0, cx: 152, cy: 246 },
        { id: 1, cx: 142, cy: 216 },
        { id: 2, cx: 176, cy: 218 },
        { id: 3, cx: 118, cy: 200 },
        { id: 4, cx: 186, cy: 250 },
        { id: 5, cx: 140, cy: 138 },
        { id: 6, cx: 172, cy: 294 },
        { id: 7, cx: 142, cy: 160 },
        { id: 8, cx: 180, cy: 158 },
        { id: 9, cx: 146, cy: 102 },
        { id: 10, cx: 188, cy: 102 },
        { id: 11, cx: 160, cy: 38 },
        { id: 12, cx: 198, cy: 38 },
        { id: 13, cx: 160, cy: 218 }
    ];
    setPoints(newPoints);
    drawLines(svg, newPoints);
    updateKeypoints(svg, newPoints); // Cập nhật vị trí các điểm keypoints trên SVG
    updateKeypointsTextarea(newPoints);
    updateInpKeypointsTextarea(svg, newPoints)
}

// Hàm thay đổi tọa độ các điểm keypoint cho tư thế Touch Head
function setTouchHead(svg, setPoints) {
    const newPoints = [
        { id: 0, cx: 176, cy: 100 },
        { id: 1, cx: 150, cy: 130 },
        { id: 2, cx: 202, cy: 135 },
        { id: 3, cx: 126, cy: 70 },
        { id: 4, cx: 241, cy: 93 },
        { id: 5, cx: 173, cy: 77 },
        { id: 6, cx: 197, cy: 70 },
        { id: 7, cx: 145, cy: 203 },
        { id: 8, cx: 190, cy: 207 },
        { id: 9, cx: 137, cy: 271 },
        { id: 10, cx: 202, cy: 272 },
        { id: 11, cx: 116, cy: 320 },
        { id: 12, cx: 192, cy: 321 },
        { id: 13, cx: 174, cy: 128 }
    ];
    setPoints(newPoints);
    drawLines(svg, newPoints);
    updateKeypoints(svg, newPoints); // Cập nhật vị trí các điểm keypoints trên SVG
    updateKeypointsTextarea(newPoints);
    updateInpKeypointsTextarea(svg, newPoints)
}

// Hàm thay đổi tọa độ các điểm keypoint cho tư thế Touch Head
function setDefault(svg, setPoints) {
    const newPoints = [
        { id: 0, cx: 160, cy: 30 },
        { id: 1, cx: 132, cy: 60 },
        { id: 2, cx: 188, cy: 60 },
        { id: 3, cx: 108, cy: 98 },
        { id: 4, cx: 216, cy: 106 },
        { id: 5, cx: 112, cy: 164 },
        { id: 6, cx: 208, cy: 164 },
        { id: 7, cx: 144, cy: 154 },
        { id: 8, cx: 184, cy: 154 },
        { id: 9, cx: 126, cy: 230 },
        { id: 10, cx: 196, cy: 230 },
        { id: 11, cx: 122, cy: 300 },
        { id: 12, cx: 200, cy: 300 },
        { id: 13, cx: 160, cy: 60 }
    ];
    setPoints(newPoints);
    drawLines(svg, newPoints);
    updateKeypoints(svg, newPoints); // Cập nhật vị trí các điểm keypoints trên SVG
    updateKeypointsTextarea(newPoints);
    updateInpKeypointsTextarea(svg, newPoints)
}

function updateKeypointsTextarea(points) {
    const textarea = document.getElementById("keypoints");
    if (textarea) {
        let keypointsText = "";
        points.forEach(point => {
            keypointsText += `${Keypoint_names[point.id]}, CX: ${point.cx}, CY: ${point.cy}\n`;
        });
        textarea.value = keypointsText;
    }
}

function updateInpKeypointsTextarea(svg, points) {
    const textarea = document.getElementById("inp_keypoints");
    if (textarea) {
        const svgRect = svg.getBoundingClientRect();
        let inpkeypointsText = [svgRect.width, svgRect.height];
        points.forEach(point => {
            inpkeypointsText.push((point.cx/svgRect.width).toFixed(4), (point.cy/svgRect.height).toFixed(4), 1.0);
        });
        textarea.value = inpkeypointsText.slice(0, inpkeypointsText.length - 3);
    }
}


// Hàm chính của ứng dụng
function initApp() {
    const svg = document.getElementById("pose-svg");
    const points = DEFAULT_POINTS;
    const [svgWidth, svgHeight] = [svg.getAttribute("width"), svg.getAttribute("height")];

    // Định nghĩa hàm setPoints
    function setPoints(newPoints) {
        // Cập nhật các điểm keypoint
        points.splice(0, points.length, ...newPoints);
    }

    // Vẽ các điểm keypoint và các đường nối
    drawPoints(svg, points, setPoints); // Fix: Truyền setPoints vào hàm drawPoints
    drawLines(svg, points);

    // Sự kiện click nút Default
    document.getElementById("btn-default").addEventListener("click", function() {
        // drawPoints(svg, DEFAULT_POINTS, setPoints);
        // drawLines(svg, DEFAULT_POINTS);
        setDefault(svg, setPoints)
    });

    // Sự kiện click nút Hands Folded
    document.getElementById("btn-hands-folded").addEventListener("click", function() {
        setArmsFolded(svg, setPoints);
    });

    // Sự kiện click nút Upside Down
    document.getElementById("btn-upside-down").addEventListener("click", function() {
        setUpSideDown(svg, setPoints);
    });

    // Sự kiện click nút Touch Head
    document.getElementById("btn-touch-head").addEventListener("click", function() {
        setTouchHead(svg, setPoints);
    });
}

// Khởi tạo ứng dụng khi trang đã được load hoàn toàn
window.addEventListener("load", initApp);
