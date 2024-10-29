function calculate_corner_points()
    % 循环读取文件并计算3D坐标
    for i = 1:30  % 假设有30对Li和Ri文件
        L_filepath = sprintf('D:\\Python Project\\solve_chessboard_corners\\corners_coordinate\\L%d.txt', i);
        R_filepath = sprintf('D:\\Python Project\\solve_chessboard_corners\\corners_coordinate\\R%d.txt', i);

        L_corners = reading_corner_points(L_filepath);
        R_corners = reading_corner_points(R_filepath);

        % 初始化变量
        disparity = [];
        depth_zc = [];
        xc = [];
        yc = [];

        % Data from Rectify_data.txt
        new_L_cameraM_data = [4413.241151745528, 0, 999.6666069030762;
                              0, 4413.241151745528, 754.5508880615234;
                              0, 0, 1];

        R1_data = [0.9871122317558534, -0.0004878743207341066, 0.1600287595922235;
                   0.0005765298903030708, 0.9999997049937958, -0.0005075683276546083;
                   -0.1600284647531934, 0.0005932882678927674, 0.9871122218257492];
        R1 = R1_data;
        inverse_R1 = inv(R1);

        % Data from P1, P2 CALCULATED BY STEREORECTIFY in Rectify_data
        pixel_focus_re = 4413.241151745528;  % From P1, element (1,1)
        f_Tx = 712741.2809573434;            % From P2, element (1,4)

        % From R1(1,3), (2,3)
        u0 = 999.6666069030762;
        v0 = 754.5508880615234;
        base_line_re = f_Tx / pixel_focus_re;

        % 计算左相机坐标系下3D坐标
        for j = 1:length(L_corners)
            disparity_now = L_corners(j,1) - R_corners(j,1);
            depth_zc_now = (pixel_focus_re * base_line_re) / disparity_now;
            xc_now = depth_zc_now * (L_corners(j,1) - u0) / pixel_focus_re;
            yc_now = depth_zc_now * (R_corners(j,2) - v0) / pixel_focus_re;
            disparity(end+1) = disparity_now;
            depth_zc(end+1) = depth_zc_now;
            xc(end+1) = xc_now;
            yc(end+1) = yc_now;
        end

        % 左相机矫正后坐标系里面的3D坐标
        point_3d_re = [xc; yc; depth_zc];

        % 左相机原坐标系的3D坐标
        point_3d_or = inverse_R1 * point_3d_re;

        % 将结果输出到Excel文件的第i个工作表
        filename = '3d_coordinates.xlsx';
        sheet_name = sprintf('Sheet%d', i);
        writematrix(point_3d_or', filename, 'Sheet', sheet_name);

        disp(['Coordinates for L' num2str(i) ' and R' num2str(i) ' has been written to ', filename, ' in ', sheet_name]);
    end
end

function points = reading_corner_points(filepath)
    points = [];
    fileID = fopen(filepath, 'r');
    if fileID == -1
        error('Cannot open file: %s', filepath);
    end
    while ~feof(fileID)
        line = fgetl(fileID);
        data = sscanf(line, '%f %f');
        if length(data) == 2
            points(end+1, :) = data';
        else
            disp('Error reading coordinates from line');
        end
    end
    fclose(fileID);
end
