package org.cnlab.crawler.model;

import net.sourceforge.jtds.jdbc.DateTime;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/2/8
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class BaseModel {
    public DateTime getVersion() {
        return version;
    }

    public void setVersion(DateTime version) {
        this.version = version;
    }

    public DateTime version;
}
