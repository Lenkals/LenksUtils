import com.sun.net.httpserver.HttpContext;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpsConfigurator;
import com.sun.net.httpserver.HttpsServer;
import com.sun.net.httpserver.HttpsParameters;

import javax.net.ssl.KeyManagerFactory;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLParameters;
import javax.net.ssl.TrustManagerFactory;
import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.security.KeyStore;

public class JVMHttpsServer {
    public static void main(String[] args) throws Exception {
        // Load the SSL/TLS certificate
        KeyStore ks = KeyStore.getInstance("JKS");
        ks.load(JVMHttpsServer.class.getResourceAsStream("/keystore.jks"), "test123".toCharArray());

        // Initialize the SSL context
        KeyManagerFactory kmf = KeyManagerFactory.getInstance("SunX509");
        kmf.init(ks, "test123".toCharArray());
        TrustManagerFactory tmf = TrustManagerFactory.getInstance("SunX509");
        tmf.init(ks);
        SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(kmf.getKeyManagers(), tmf.getTrustManagers(), null);

        // Create the HTTPS server
        HttpsServer server = HttpsServer.create(new InetSocketAddress(8443), 0);
        server.setHttpsConfigurator(new HttpsConfigurator(sslContext) {
            public void configure(HttpsParameters params) {
                SSLContext c = getSSLContext();
                SSLParameters sslParams = c.getDefaultSSLParameters();
                params.setSSLParameters(sslParams);
            }
        });

        HttpContext context = server.createContext("/");
        context.setHandler(JVMHttpsServer::handleRequest);
        server.start();
        System.out.println("JVM HTTPS server started on port 8443");
    }

    private static void handleRequest(HttpExchange exchange) throws IOException {
        String response = "Hello from the JVM HTTPS server!";
        exchange.sendResponseHeaders(200, response.getBytes().length);
        OutputStream os = exchange.getResponseBody();
        os.write(response.getBytes());
        os.close();
    }
}
