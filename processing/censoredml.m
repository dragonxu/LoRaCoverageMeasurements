% CENSOREDML Numerical maximum-likelihood estimation of a censored normal
% distribtuion.
%
%   CENSOREDML(X,Y,C,T,A,S2) performs a numerical optimization of the parameters
%   for the log-likelihood of a censored normal distribution.
%   The data is assumed to be of the form Y=alpha*X+e, where alpha are regression
%   coefficients and e is r.v. that is Gaussian with zero mean.
%
%   C is a constant describing the censoring level and T is a vector indicating if
%   the samples are censored or uncensored (0 indicates that the sample is
%   censored and 1 indicates that it is uncensored). A and S are initial values for
%   the regression parameters and the variance of the error, respectively.
%   For pathloss estimation, A contains the initial values of [PL(d0); n] and S is
%   the initial value of the large scale fading variance sigma2. If You use this 
%   code, or parts of it, please cite the following paper: 
%   C. Gustafson, T. Abbas, D. Bolin and F. Tufvesson,
%   "Statistical Modeling and Estimation of Censored Pathloss Data",
%   IEEE Wireless Communications Letters, 2015.
%
%   Copyright (C) 2015, David Bolin, Carl Gustafson.
%
%   This program is free software: you can redistribute it and/or modify
%   it under the terms of the GNU General Public License as published by
%   the Free Software Foundation, either version 3 of the License, or
%   (at your option) any later version.
%
%   This program is distributed in the hope that it will be useful,
%   but WITHOUT ANY WARRANTY; without even the implied warranty of
%   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%   GNU General Public License for more details.
%
%   You should have received a copy of the GNU General Public License
%   along with this program.  If not, see <http://www.gnu.org/licenses/>.

function est=censoredml(d,y,c,t,a_est,s2e)

  opts = optimset('GradObj','off', 'Largescale','off','MaxFunEvals',20000,'MaxIter',20000);
  PL0 = a_est(1)
  n = a_est(2)
  pars = fminsearch(@(pars) censoredllh(pars),[PL0;n;sqrt(s2e)],opts);
  est = pars;

  function l = censoredllh(p)
    L = zeros(size(y));
    PL0 = p(1);
    n = p(2);
    sigma = p(3);

    PLm = 10*n*log10(d(t==1)') + PL0;
    PLm_star = 10*n*log10(d(t==0)') + PL0;

    L(t==1) = -log(sigma) + log(normpdf((y(t==1)-PLm)./sigma));

    L(t==0)= log(1-normcdf((c-PLm_star)./sigma));
    l = -sum(L);
  end
end