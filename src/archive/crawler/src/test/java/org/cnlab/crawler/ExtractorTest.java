package org.cnlab.crawler;

import junit.framework.TestCase;

import java.io.File;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/10
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class ExtractorTest extends TestCase {
    public void testStartIndexing()
    {
        File crawlerPath = new File("D:\\hybwps\\muser\\crawler\\src\\test");
        File[] crawlerFold = new File[]{crawlerPath};
        Extractor.startIndexing(crawlerFold);
    }
}
