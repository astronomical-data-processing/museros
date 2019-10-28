package org.cnlab.commno.test.utils;

import junit.framework.TestCase;
import org.cnlab.common.utils.CommonHelper;

/**
 * @Project: muser
 * @Author: cnlab
 * @Date: 2015/1/30
 * @Copyright: 2015.CNNEB All rights reserved.
 * To change this template use File | Settings | File Templates.
 */
public class CommonHelperTest extends TestCase {
    public void testUUID() {
        String uuid = CommonHelper.getUUID();
        TestCase.assertEquals(36, uuid.length());
    }

    public void testRandom() {
        String randomStr = CommonHelper.getFixLenthString(8);
        TestCase.assertEquals(8, randomStr.length());
    }

    //21232f297a57a5a743894a0e4a801fc3
    public void testGetMD5() {
        String plainText = "admin";
        String md5 = CommonHelper.getMD5(plainText);
        TestCase.assertEquals("21232f297a57a5a743894a0e4a801fc3", md5);
    }
}
