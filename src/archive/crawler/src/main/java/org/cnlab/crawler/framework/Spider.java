package org.cnlab.crawler.framework;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/8
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public interface Spider {
    public void crawl(SpiderContext context);
}
