CREATE TABLE `CBN_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT 'id',
  `province` varchar(30) DEFAULT NULL COMMENT '省份',
  `city` varchar(30) DEFAULT NULL COMMENT '城市',
  `district` varchar(30) DEFAULT NULL COMMENT '行政区',
  `address` varchar(100) DEFAULT NULL COMMENT '地址',
  `longitude` float DEFAULT NULL COMMENT '经度',
  `latitude` float DEFAULT NULL COMMENT '纬度',
  `count` varchar(10) DEFAULT NULL COMMENT '确诊数量',
  `hash_value` varchar(50) NOT NULL COMMENT '去重hash值',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间',
  `update_time` datetime DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `hash_value` (`hash_value`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='CBNdata疫情地图数据';