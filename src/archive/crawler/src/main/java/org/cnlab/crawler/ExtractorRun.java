package org.cnlab.crawler;

import java.io.File;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/10
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class ExtractorRun {
    public static void main(String[] args) {
        File crawlerPath = new File("D:\\hybwps\\muser");
        File[] crawlerFold = new File[]{crawlerPath};
        Extractor.startIndexing(crawlerFold);
    }
}
