#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QImage>
#include <QDebug>
#include<opencv2\opencv.hpp>
#include<iostream>
#include <imgproc\types_c.h>

using namespace cv;
using namespace std;
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    connect(ui->pushButton, SIGNAL(clicked(bool)), this, SLOT(OpenImg()));
    connect(ui->pushButton_2, SIGNAL(clicked(bool)), this, SLOT(processimage()));
}
QString OpenFile, OpenFilePath, OpenFilePath2;
void MainWindow::OpenImg()
{
    QImage image;
    //打开文件夹中的图片文件
    OpenFile = QFileDialog::getOpenFileName(this,
                                              "Please choose an image file",
                                              "",
                                              "Image Files(*.jpg *.png *.bmp *.pgm *.pbm *.tif);;All(*.*)");
    if( OpenFile != "" )
    {
        if( image.load(OpenFile) )
        {
            ui->label->setPixmap(QPixmap::fromImage(image));
            ui->label->setScaledContents(true);
        }
    }

    //显示所示图片的路径
    QFileInfo OpenFileInfo;
    OpenFileInfo = QFileInfo(OpenFile);
    OpenFilePath = OpenFileInfo.filePath();
    OpenFilePath2 = OpenFileInfo.absolutePath();
    ui->lineEdit->setText(OpenFilePath);
}
bool findNextPoint(vector<Point>& _neighbor_points, Mat& _image, Point _inpoint, int flag, Point& _outpoint, int& _outflag)
{
    int i = flag;
    int count = 1;
    bool success = false;

    while (count <= 8)
    {
        Point tmppoint = _inpoint + _neighbor_points[i];
        if (tmppoint.x > 0 && tmppoint.y > 0 && tmppoint.x < _image.cols && tmppoint.y < _image.rows)
        {
            if (_image.at<uchar>(tmppoint) == 255)
            {
                _outpoint = tmppoint;
                _outflag = i;
                success = true;
                _image.at<uchar>(tmppoint) = 0;
                break;
            }
        }
        if (count % 2)
        {
            i += count;
            if (i > 7)
            {
                i -= 8;
            }
        }
        else
        {
            i += -count;
            if (i < 0)
            {
                i += 8;
            }
        }
        count++;
    }
    return success;
}
//寻找图像上的第一个点
bool findFirstPoint(Mat& _inputimg, Point& _outputpoint)
{
    bool success = false;
    for (int i = 0; i < _inputimg.rows; i++)
    {
        uchar* data = _inputimg.ptr<uchar>(i);
        for (int j = 0; j < _inputimg.cols; j++)
        {
            if (data[j] == 255)
            {
                success = true;
                _outputpoint.x = j;
                _outputpoint.y = i;
                data[j] = 0;
                break;
            }
        }
        if (success)
            break;
    }
    return success;
}
//寻找曲线
void findLines(Mat& _inputimg, vector<deque<Point>>& _outputlines)
{
    vector<Point> neighbor_points = { Point(-1,-1),Point(0,-1),Point(1,-1),Point(1,0),Point(1,1),Point(0,1),Point(-1,1),Point(-1,0) };
    Point first_point;
    //int s = 0;
    while (findFirstPoint(_inputimg, first_point))
    {
        deque<Point> line;
        line.push_back(first_point);
        //由于第一个点不一定是线段的起始位置，双向找
        Point this_point = first_point;
        int this_flag = 0;
        Point next_point;
        int next_flag;
        while (findNextPoint(neighbor_points, _inputimg, this_point, this_flag, next_point, next_flag))
        {
            line.push_back(next_point);
            this_point = next_point;
            this_flag = next_flag;
        }
        //找另一边
        this_point = first_point;
        this_flag = 0;
        while (findNextPoint(neighbor_points, _inputimg, this_point, this_flag, next_point, next_flag))
        {
            line.push_front(next_point);
            this_point = next_point;
            this_flag = next_flag;

        }
        if (line.size() > 0)
        {
            _outputlines.push_back(line);
        }
    }
}
//随机取色 用于画线的时候
Scalar random_color(RNG& _rng)
{
    int icolor = (unsigned)_rng;
    return Scalar(icolor & 0xFF, (icolor >> 8) & 0xFF, (icolor >> 16) & 0xFF);
}
int MainWindow::processimage()
{
    Mat image = imread(OpenFilePath.toUtf8().data());
    Mat gray;
    cvtColor(image, gray, CV_BGR2GRAY);
    vector<deque<Point>> lines;
    findLines(gray, lines);
    //cout << lines.size() << endl;
    //draw lines
    Mat draw_img = image.clone();
    RNG rng(123);
    Scalar color;
    int s = 0;
    for (int i = 0; i < lines.size(); i++)
    {
        if (lines[i].size() > 20)//上色
        {
            color = random_color(rng);
            for (int j = 0; j < lines[i].size(); j++)
            {
                draw_img.at<Vec3b>(lines[i][j]) = Vec3b(color[0], color[1], color[2]);
            }
        }
        if (lines[i].size() <= 20)//显示
        {
            for (int j = 0; j < lines[i].size(); j++)
            {
                draw_img.at<Vec3b>(lines[i][j]) = Vec3b(0, 0, 0);
            }
        }
        if (lines[i].size() > 20)//标号
        {
            s++;
            QString num = QString::number(s);
            QString length = QString::number(lines[i].size());
            ui->textEdit->append(num+QString(":")+length);
            string m = to_string(s);
            int x = (lines[i].size()) / 2;
            putText(draw_img, m, Point(lines[i][x]), FONT_HERSHEY_SCRIPT_SIMPLEX, 0.35, Scalar(255, 255, 255), 1);
        }
    }
    OpenFilePath2 += " Result.tif";
    imwrite(OpenFilePath2.toUtf8().data(), draw_img);
    Mat temp;
    cvtColor(draw_img, temp, CV_BGR2RGB);//BGR convert to RGB
    QImage Qtemp = QImage((const unsigned char*)(temp.data), temp.cols, temp.rows, temp.step, QImage::Format_RGB888);
    ui->label->setPixmap(QPixmap::fromImage(Qtemp));
    ui->label->setScaledContents(true);
    waitKey(0);
    system("pause");
    return 0;
}

MainWindow::~MainWindow()
{
    delete ui;
}

