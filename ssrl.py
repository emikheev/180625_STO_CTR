def angles2HKL(angles,anglescorr,a,b,c,Lambda):
    import numpy
    from numpy import cos
    from numpy import sin
    from math import pi
    
    wavevector=2*pi/Lambda; #wavevector in 1/A
    dgamma=numpy.radians(anglescorr[0]);
    dtth=numpy.radians(anglescorr[1]);

    th=numpy.radians(angles[0]);
    tth=numpy.radians(angles[1])+dtth;
    chi=numpy.radians(angles[2]-90);
    phi=numpy.radians(180-angles[3]);
    gamma=0+dgamma;

    H = 0.159154943091895*a*wavevector*((cos(gamma)*cos(tth) - 1)*((-sin(phi)**2 + 1)*sin(chi)*sin(th)/cos(phi) + (-sin(th)**2 + 1)*sin(phi)/cos(th)) + (-(-sin(phi)**2 + 1)*sin(chi)*cos(th)/cos(phi) + sin(phi)*sin(th))*sin(tth)*cos(gamma) - (-sin(chi)**2 + 1)*(-sin(phi)**2 + 1)*sin(gamma)/(cos(chi)*cos(phi)))
    K = 0.159154943091895*b*wavevector*((cos(gamma)*cos(tth) - 1)*((-sin(th)**2 + 1)*cos(phi)/cos(th) - sin(chi)*sin(phi)*sin(th)) + (sin(chi)*sin(phi)*cos(th) + sin(th)*cos(phi))*sin(tth)*cos(gamma) + (-sin(chi)**2 + 1)*sin(gamma)*sin(phi)/cos(chi))
    L = 0.159154943091895*c*wavevector*(-(cos(gamma)*cos(tth) - 1)*sin(th)*cos(chi) - sin(chi)*sin(gamma) + sin(tth)*cos(chi)*cos(gamma)*cos(th))
    HKL=numpy.array([H,K,L])

    return HKL


def PDIimp(filenamePDI):
    f2 = open(filenamePDI)
    PDI=f2.read() 
    f2.close()
    k1=PDI.find("Theta = ");
    k2=PDI.find("Gamma");
    m_angle=PDI[k1:k2-1];
    m_angle=m_angle.replace('2Theta','TwoTheta')
    exec('global Theta; global TwoTheta; global Chi; global Phi;'+m_angle)
    angles=Theta, TwoTheta, Chi, Phi;
    k1=PDI.find("LAMBDA = ");
    k2=PDI.find("# Initial");
    m_lambda=PDI[k1:k2-1];
    exec('global LAMBDA;'+m_lambda)
    return angles, LAMBDA

def fLorentz(angles):
    import numpy as np
    th=np.radians(angles[0]);
    tth=np.radians(angles[1]);
    chi=np.radians(angles[2]);
    f=1/(np.sin(tth-th)*np.sin(chi))
    return f

def fIA(angles,fwhmV,fwhmH,samplesize):    
    from scipy import integrate
    import numpy as np
    sigmaV=fwhmV/2.35;
    sigmaH=fwhmH/2.35;
    th=np.radians(angles[0]);
    #tth=np.radians(angles[1]);
    chi=np.radians(angles[2]);
    phi=np.radians(angles[3]);
    
    xlab = lambda x, y, th, chi, phi: (np.cos(th)*np.cos(chi)*np.cos(phi)-np.sin(th)*np.sin(phi))*x+(np.cos(phi)*np.sin(th)+np.cos(th)*np.cos(chi)*np.sin(phi))*y;
    zlab = lambda x, y, chi, phi: -np.cos(phi)*np.sin(chi)*x-np.sin(phi)*np.sin(chi)*y;
    beam = lambda x, y: 1/2/np.pi/sigmaH/sigmaV*np.exp(-xlab(x, y, th, chi, phi)**2/2/sigmaV**2)*np.exp(-zlab(x, y, chi, phi)**2/2/sigmaH**2)
    f=integrate.dblquad(beam, samplesize[0], samplesize[1], lambda x: samplesize[2], lambda x: samplesize[3],epsrel=1e0)    
    return f[0]



