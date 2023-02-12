#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QFileDialog>
#include <QFileInfo>
#include <QImage>
#include <opencv2/opencv.hpp>
#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QImage>
#include <QDebug>
#include <opencv2\opencv.hpp>
#include <iostream>
#include <imgproc\types_c.h>

using namespace cv;
using namespace std;

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private slots:
    void OpenImg();
    int processimage();


private:
    Ui::MainWindow *ui;
};

#endif // MAINWINDOW_H

