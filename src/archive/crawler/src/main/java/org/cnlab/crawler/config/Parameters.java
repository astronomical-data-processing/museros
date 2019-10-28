package org.cnlab.crawler.config;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/8
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class Parameters {
    public Parameters(String[] values) {
        this.values = values;
    }

    public String[] getValues() {
        return values;
    }

    protected String[] values;

}
