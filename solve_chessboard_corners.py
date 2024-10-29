import cv2
import glob
def reorder_points(points, row_num):
    if len(points) % row_num != 0:
        print("The total number of points is not a multiple of col_corner.")
        return points

    for i in range(0, len(points), row_num):
        # 使用列表切片和反转
        points[i:i + row_num] = points[i:i + row_num][::-1]

    return points


def get_corner_point_coordinate(chessboard, img, i):
    size = (chessboard[0], chessboard[1])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 检测棋盘格角点
    success, corner_pts = cv2.findChessboardCorners(
        gray, size,
        cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE
    )

    if success:
        # 亚像素角点检测
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_COUNT, 30, 1e-6)
        cv2.cornerSubPix(gray, corner_pts, (11, 11), (-1, -1), criteria)

        # 重新排列角点
        corner_pts = reorder_points(corner_pts, chessboard[0])
        cv2.putText(img,"corners count:"+ str(corner_pts.shape[0]), (220,220), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 34, 178), 2)

        for i in range(len(corner_pts)):
            # 将坐标转换为整数
            x, y = int(corner_pts[i][0][0]), int(corner_pts[i][0][1])
            cv2.putText(img, str(i + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (34, 34, 178), 2)

        # 绘制棋盘角点
        cv2.drawChessboardCorners(img, size, corner_pts, success)
        cv2.imshow("image pair corner_pt_detection", cv2.resize(img, (img.shape[1] // 2, img.shape[0] // 2)))
        cv2.waitKey(0)

        return corner_pts

    else:
        print("Reject pair "+str(i+1))

        return []


def output_corners_coordinate(corners1, corners2, i):
    with open("corners_coordinate/"+"L"+str(i+1)+".txt", "w") as output_corners1:
        for corner in corners1:
            output_corners1.write(f"{corner[0][0]} {corner[0][1]}\n")

    with open("corners_coordinate/"+"R"+str(i+1)+".txt", "w") as output_corners2:
        for corner in corners2:
            output_corners2.write(f"{corner[0][0]} {corner[0][1]}\n")


def main():
    chessboard = (8, 11)

    L_path = "L_images/*.bmp"
    R_path = "R_images/*.bmp"
    L_images = [cv2.imread(file) for file in glob.glob(L_path)]
    R_images = [cv2.imread(file) for file in glob.glob(R_path)]

    for i in range(len(L_images)):
        # 读取矫正后的左,右图像
        left_img = L_images[i]
        right_img = R_images[i]
        if left_img is None or right_img is None:
            print("Error: Could not open or find the images!")
            return

        print(f"image size: {left_img.shape[0:2]}"+"image pair: " + str(i+1))

        # 检测并显示角点
        left_corner_pts = get_corner_point_coordinate(chessboard, left_img, i)
        right_corner_pts = get_corner_point_coordinate(chessboard, right_img, i)

        output_corners_coordinate(left_corner_pts, right_corner_pts, i)


if __name__ == "__main__":
    main()
