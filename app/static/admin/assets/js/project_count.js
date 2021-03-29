$.get('/admin/project_count').done(function (data) {
    var myChart = echarts.init(document.getElementById('project_count'), 'macarons');
    myChart.setOption({
        title: {
            text: '每月项目数量',
            subtext: data.this_year + '年度'
        },
        tooltip: {
            trigger: 'axis'
        },
        toolbox: {
            show: true,
            feature: {
                dataZoom: {
                    yAxisIndex: 'none'
                },
                dataView: {readOnly: false},
                magicType: {type: ['line', 'bar']},
                restore: {},
                saveAsImage: {}
            }
        },
        xAxis: {
            type: 'category',
            boundaryGap: false,
            data: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                formatter: '{value} 个'
            }
        },
        series: [
            {
                name: '项目数',
                type: 'line',
                data: data.num,
                markPoint: {
                    data: [
                        {type: 'max', name: '最大值'},
                        {type: 'min', name: '最小值'}
                    ]
                },
                markLine: {
                    data: [
                        {type: 'average', name: '平均值'}
                    ]
                }
            }
        ]
    });
});