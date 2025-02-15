<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
        <head>
            <title>OxyClient Server UI</title>
            <style>
                body { font-family: Arial, sans-serif; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
                th { background-color: #333; color: white; }
                .online { color: green; font-weight: bold; }
                .offline { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>OxyClient Server Status</h1>
            <table>
                <tr>
                    <th>Server Name</th>
                    <th>Status</th>
                    <th>Connected Users</th>
                </tr>
                <xsl:for-each select="servers/server">
                    <tr>
                        <td><xsl:value-of select="name"/></td>
                        <td>
                            <xsl:choose>
                                <xsl:when test="status='Online'">
                                    <span class="online">Online</span>
                                </xsl:when>
                                <xsl:otherwise>
                                    <span class="offline">Offline</span>
                                </xsl:otherwise>
                            </xsl:choose>
                        </td>
                        <td>
                            <xsl:for-each select="users/user">
                                <xsl:value-of select="."/><br/>
                            </xsl:for-each>
                        </td>
                    </tr>
                </xsl:for-each>
            </table>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>
