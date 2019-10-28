package org.cnlab.crawler.test;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/10
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class Run {
    public static void main(String[] args) {
        BlockingQueue<String> queue = new LinkedBlockingQueue<String>(8);
        new Thread(new Producer(queue)).start();
        new Thread(new Consumer(queue)).start();
        System.out.println("主线程退出");
    }
}
